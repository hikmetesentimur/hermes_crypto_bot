import asyncio
from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import pytest

from hermes_crypto_bot.domain.exchange_capabilities import (
    CapabilityManifest,
    EnvironmentCapabilities,
    OrderCapabilities,
    OrderType,
    ProductCapabilities,
    TimeInForce,
    TradingEnvironment,
    TradingProduct,
)
from hermes_crypto_bot.domain.exchange_symbols import (
    NotionalFormula,
    OrderSymbolRules,
    SymbolMetadata,
    SymbolTradingStatus,
)
from hermes_crypto_bot.ports.exchange_metadata import (
    ExchangeAdapterError,
    ExchangeAdapterErrorCode,
    ExchangeAdapterOperation,
    ExchangeMetadataPort,
    MetadataContractError,
    MetadataViolationCode,
    validate_metadata_snapshot,
)


def order_capability(order_type: OrderType) -> OrderCapabilities:
    return OrderCapabilities(
        order_type=order_type,
        time_in_force=frozenset()
        if order_type is OrderType.MARKET
        else frozenset({TimeInForce.GTC}),
        supports_post_only=False,
        supports_reduce_only=False,
        native_protections=frozenset(),
        position_modes=frozenset(),
    )


def environment(
    environment_name: TradingEnvironment,
    *order_types: OrderType,
) -> EnvironmentCapabilities:
    return EnvironmentCapabilities(
        environment=environment_name,
        orders=tuple(order_capability(item) for item in order_types),
        candle_intervals=frozenset({"1m"}),
    )


def manifest(*products: ProductCapabilities) -> CapabilityManifest:
    return CapabilityManifest(
        schema_version=1,
        exchange_code="fixture-exchange",
        products=products,
    )


def product(
    product_name: TradingProduct,
    *environments: EnvironmentCapabilities,
) -> ProductCapabilities:
    return ProductCapabilities(product=product_name, environments=environments)


def rules(order_type: OrderType) -> OrderSymbolRules:
    if order_type is OrderType.MARKET:
        return OrderSymbolRules(
            order_type=order_type,
            quantity_step=Decimal("0.001"),
            min_quantity=Decimal("0.001"),
            max_quantity=None,
            price_tick=None,
            min_price=None,
            max_price=None,
            min_notional=None,
            max_notional=None,
        )
    return OrderSymbolRules(
        order_type=order_type,
        quantity_step=Decimal("0.001"),
        min_quantity=Decimal("0.001"),
        max_quantity=None,
        price_tick=Decimal("0.1"),
        min_price=None,
        max_price=None,
        min_notional=None,
        max_notional=None,
    )


def symbol(
    *,
    exchange_code: str = "fixture-exchange",
    capability_schema_version: int = 1,
    snapshot_id: str = "fixture-snapshot-1",
    observed_at: datetime = datetime(2026, 7, 26, 16, 0, tzinfo=UTC),
    environment_name: TradingEnvironment = TradingEnvironment.TESTNET,
    product_name: TradingProduct = TradingProduct.SPOT,
    exchange_symbol: str = "BTCUSDT",
    order_type: OrderType = OrderType.LIMIT,
) -> SymbolMetadata:
    return SymbolMetadata(
        exchange_code=exchange_code,
        capability_schema_version=capability_schema_version,
        snapshot_id=snapshot_id,
        observed_at=observed_at,
        environment=environment_name,
        product=product_name,
        exchange_symbol=exchange_symbol,
        base_asset="BTC",
        quote_asset="USDT",
        status=SymbolTradingStatus.TRADING,
        notional_formula=(
            NotionalFormula.SPOT
            if product_name is TradingProduct.SPOT
            else NotionalFormula.LINEAR_CONTRACT
        ),
        contract_size=None if product_name is TradingProduct.SPOT else Decimal("0.001"),
        order_rules=(rules(order_type),),
    )


def supported_manifest() -> CapabilityManifest:
    return manifest(
        product(
            TradingProduct.SPOT,
            environment(TradingEnvironment.TESTNET, OrderType.LIMIT),
        )
    )


def test_metadata_snapshot_is_validated_and_defensively_copied() -> None:
    source = [symbol()]

    snapshot = validate_metadata_snapshot(
        manifest=supported_manifest(),
        environment=TradingEnvironment.TESTNET,
        product=TradingProduct.SPOT,
        symbols=source,
    )
    source.clear()

    assert snapshot == (symbol(),)


@pytest.mark.parametrize("symbols", ["BTCUSDT", b"BTCUSDT", None, ("BTCUSDT",)])
def test_metadata_snapshot_rejects_malformed_collections(symbols: Any) -> None:
    with pytest.raises(ValueError, match="metadata"):
        validate_metadata_snapshot(
            manifest=supported_manifest(),
            environment=TradingEnvironment.TESTNET,
            product=TradingProduct.SPOT,
            symbols=symbols,
        )


def test_unknown_product_stops_before_inspecting_symbol_details() -> None:
    with pytest.raises(MetadataContractError) as captured:
        validate_metadata_snapshot(
            manifest=supported_manifest(),
            environment=TradingEnvironment.LIVE,
            product=TradingProduct.FUTURES,
            symbols=(
                symbol(
                    exchange_code="other-exchange",
                    environment_name=TradingEnvironment.LIVE,
                    product_name=TradingProduct.FUTURES,
                    order_type=OrderType.MARKET,
                ),
            ),
        )

    assert captured.value.violations == (MetadataViolationCode.PRODUCT_UNSUPPORTED,)


def test_unknown_environment_stops_before_inspecting_order_filters() -> None:
    with pytest.raises(MetadataContractError) as captured:
        validate_metadata_snapshot(
            manifest=supported_manifest(),
            environment=TradingEnvironment.LIVE,
            product=TradingProduct.SPOT,
            symbols=(
                symbol(
                    environment_name=TradingEnvironment.LIVE,
                    order_type=OrderType.MARKET,
                ),
            ),
        )

    assert captured.value.violations == (MetadataViolationCode.ENVIRONMENT_UNSUPPORTED,)


def test_environment_from_another_product_does_not_leak() -> None:
    capabilities = manifest(
        product(
            TradingProduct.SPOT,
            environment(TradingEnvironment.SANDBOX, OrderType.MARKET),
        ),
        product(
            TradingProduct.FUTURES,
            environment(TradingEnvironment.LIVE, OrderType.LIMIT),
        ),
    )

    with pytest.raises(MetadataContractError) as captured:
        validate_metadata_snapshot(
            manifest=capabilities,
            environment=TradingEnvironment.SANDBOX,
            product=TradingProduct.FUTURES,
            symbols=(
                symbol(
                    environment_name=TradingEnvironment.SANDBOX,
                    product_name=TradingProduct.FUTURES,
                    order_type=OrderType.MARKET,
                ),
            ),
        )

    assert captured.value.violations == (MetadataViolationCode.ENVIRONMENT_UNSUPPORTED,)


def test_order_rule_from_another_environment_does_not_leak() -> None:
    capabilities = manifest(
        product(
            TradingProduct.SPOT,
            environment(TradingEnvironment.TESTNET, OrderType.LIMIT),
            environment(TradingEnvironment.LIVE, OrderType.MARKET),
        )
    )

    with pytest.raises(MetadataContractError) as captured:
        validate_metadata_snapshot(
            manifest=capabilities,
            environment=TradingEnvironment.TESTNET,
            product=TradingProduct.SPOT,
            symbols=(symbol(order_type=OrderType.MARKET),),
        )

    assert captured.value.violations == (MetadataViolationCode.ORDER_TYPE_UNSUPPORTED,)


@pytest.mark.parametrize(
    ("candidate", "violation"),
    [
        (symbol(exchange_code="other-exchange"), MetadataViolationCode.EXCHANGE_MISMATCH),
        (
            symbol(product_name=TradingProduct.FUTURES),
            MetadataViolationCode.PRODUCT_MISMATCH,
        ),
        (
            symbol(environment_name=TradingEnvironment.LIVE),
            MetadataViolationCode.ENVIRONMENT_MISMATCH,
        ),
    ],
)
def test_snapshot_rejects_scope_mismatches(
    candidate: SymbolMetadata,
    violation: MetadataViolationCode,
) -> None:
    with pytest.raises(MetadataContractError) as captured:
        validate_metadata_snapshot(
            manifest=supported_manifest(),
            environment=TradingEnvironment.TESTNET,
            product=TradingProduct.SPOT,
            symbols=(candidate,),
        )

    assert captured.value.violations == (violation,)


def test_snapshot_rejects_duplicate_exchange_symbol() -> None:
    with pytest.raises(MetadataContractError) as captured:
        validate_metadata_snapshot(
            manifest=supported_manifest(),
            environment=TradingEnvironment.TESTNET,
            product=TradingProduct.SPOT,
            symbols=(symbol(), symbol()),
        )

    assert captured.value.violations == (MetadataViolationCode.SYMBOL_DUPLICATED,)


class FakeMetadataPort:
    @property
    def capabilities(self) -> CapabilityManifest:
        return supported_manifest()

    async def list_symbols(
        self,
        *,
        environment: TradingEnvironment,
        product: TradingProduct,
    ) -> tuple[SymbolMetadata, ...]:
        assert environment is TradingEnvironment.TESTNET
        assert product is TradingProduct.SPOT
        return (symbol(),)

    async def get_symbol_metadata(
        self,
        *,
        environment: TradingEnvironment,
        product: TradingProduct,
        exchange_symbol: str,
    ) -> SymbolMetadata:
        assert environment is TradingEnvironment.TESTNET
        assert product is TradingProduct.SPOT
        assert exchange_symbol == "BTCUSDT"
        return symbol()


def test_runtime_metadata_port_is_public_and_read_only() -> None:
    port = FakeMetadataPort()

    assert isinstance(port, ExchangeMetadataPort)
    assert asyncio.run(
        port.list_symbols(
            environment=TradingEnvironment.TESTNET,
            product=TradingProduct.SPOT,
        )
    ) == (symbol(),)
    assert (
        asyncio.run(
            port.get_symbol_metadata(
                environment=TradingEnvironment.TESTNET,
                product=TradingProduct.SPOT,
                exchange_symbol="BTCUSDT",
            )
        )
        == symbol()
    )
    assert not hasattr(ExchangeMetadataPort, "place_order")
    assert not hasattr(ExchangeMetadataPort, "get_balance")


@pytest.mark.parametrize(
    ("code", "retryable"),
    [
        (ExchangeAdapterErrorCode.RATE_LIMITED, True),
        (ExchangeAdapterErrorCode.TIMEOUT, True),
        (ExchangeAdapterErrorCode.TEMPORARILY_UNAVAILABLE, True),
        (ExchangeAdapterErrorCode.MAINTENANCE, True),
        (ExchangeAdapterErrorCode.INVALID_RESPONSE, False),
        (ExchangeAdapterErrorCode.UNSUPPORTED_SYMBOL, False),
        (ExchangeAdapterErrorCode.PERMISSION_DENIED, False),
    ],
)
def test_adapter_error_has_stable_retryability_without_raw_response(
    code: ExchangeAdapterErrorCode,
    retryable: bool,
) -> None:
    error = ExchangeAdapterError(
        exchange_code="fixture-exchange",
        operation=ExchangeAdapterOperation.LIST_SYMBOLS,
        code=code,
    )

    assert error.retryable is retryable
    assert "fixture-exchange" in str(error)
    assert not hasattr(error, "raw_response")
    with pytest.raises(FrozenInstanceError):
        error.code = ExchangeAdapterErrorCode.TIMEOUT  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("exchange_code", "bad code", "Borsa kodu"),
        ("operation", "list_symbols", "Operasyon"),
        ("code", "timeout", "Hata kodu"),
    ],
)
def test_adapter_error_rejects_untyped_fields(
    field: str,
    value: Any,
    message: str,
) -> None:
    values: dict[str, Any] = {
        "exchange_code": "fixture-exchange",
        "operation": ExchangeAdapterOperation.LIST_SYMBOLS,
        "code": ExchangeAdapterErrorCode.TIMEOUT,
    }
    values[field] = value

    with pytest.raises(ValueError, match=message):
        ExchangeAdapterError(**values)


def test_metadata_contract_error_requires_at_least_one_violation() -> None:
    with pytest.raises(ValueError, match="En az bir"):
        MetadataContractError(())


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("manifest", object(), "manifest"),
        ("environment", "testnet", "Çalışma ortamı"),
        ("product", "spot", "Ürün"),
    ],
)
def test_snapshot_rejects_unvalidated_scope_inputs(
    field: str,
    value: Any,
    message: str,
) -> None:
    values: dict[str, Any] = {
        "manifest": supported_manifest(),
        "environment": TradingEnvironment.TESTNET,
        "product": TradingProduct.SPOT,
        "symbols": (),
    }
    values[field] = value

    with pytest.raises(ValueError, match=message):
        validate_metadata_snapshot(**values)


def test_empty_metadata_snapshot_is_a_valid_immutable_snapshot() -> None:
    assert (
        validate_metadata_snapshot(
            manifest=supported_manifest(),
            environment=TradingEnvironment.TESTNET,
            product=TradingProduct.SPOT,
            symbols=[],
        )
        == ()
    )


def test_repeated_same_violation_is_reported_once() -> None:
    with pytest.raises(MetadataContractError) as captured:
        validate_metadata_snapshot(
            manifest=supported_manifest(),
            environment=TradingEnvironment.TESTNET,
            product=TradingProduct.SPOT,
            symbols=(
                symbol(exchange_symbol="BTCUSDT", order_type=OrderType.MARKET),
                symbol(exchange_symbol="ETHUSDT", order_type=OrderType.MARKET),
            ),
        )

    assert captured.value.violations == (MetadataViolationCode.ORDER_TYPE_UNSUPPORTED,)


def test_snapshot_rejects_generator_without_consuming_it() -> None:
    def unsafe_generator():
        raise AssertionError("generator must not be consumed")
        yield symbol()

    with pytest.raises(ValueError, match="list veya tuple"):
        validate_metadata_snapshot(
            manifest=supported_manifest(),
            environment=TradingEnvironment.TESTNET,
            product=TradingProduct.SPOT,
            symbols=unsafe_generator(),
        )


def test_snapshot_violations_are_stable_and_duplicates_are_scope_independent() -> None:
    first = symbol(exchange_code="other-exchange")
    second = symbol(order_type=OrderType.MARKET)
    expected = (
        MetadataViolationCode.EXCHANGE_MISMATCH,
        MetadataViolationCode.ORDER_TYPE_UNSUPPORTED,
        MetadataViolationCode.SYMBOL_DUPLICATED,
    )

    for records in ((first, second), (second, first)):
        with pytest.raises(MetadataContractError) as captured:
            validate_metadata_snapshot(
                manifest=supported_manifest(),
                environment=TradingEnvironment.TESTNET,
                product=TradingProduct.SPOT,
                symbols=records,
            )
        assert captured.value.violations == expected


def test_snapshot_requires_capability_version_and_single_snapshot_identity() -> None:
    with pytest.raises(MetadataContractError) as version_error:
        validate_metadata_snapshot(
            manifest=supported_manifest(),
            environment=TradingEnvironment.TESTNET,
            product=TradingProduct.SPOT,
            symbols=(symbol(capability_schema_version=2),),
        )
    assert version_error.value.violations == (MetadataViolationCode.CAPABILITY_VERSION_MISMATCH,)

    with pytest.raises(MetadataContractError) as snapshot_error:
        validate_metadata_snapshot(
            manifest=supported_manifest(),
            environment=TradingEnvironment.TESTNET,
            product=TradingProduct.SPOT,
            symbols=(
                symbol(exchange_symbol="BTCUSDT"),
                symbol(exchange_symbol="ETHUSDT", snapshot_id="fixture-snapshot-2"),
            ),
        )
    assert snapshot_error.value.violations == (MetadataViolationCode.SNAPSHOT_MISMATCH,)


def test_snapshot_rejects_records_above_protective_limit() -> None:
    oversized = [symbol()] * 100_001

    with pytest.raises(ValueError, match="güvenli kayıt sınırını"):
        validate_metadata_snapshot(
            manifest=supported_manifest(),
            environment=TradingEnvironment.TESTNET,
            product=TradingProduct.SPOT,
            symbols=oversized,
        )
