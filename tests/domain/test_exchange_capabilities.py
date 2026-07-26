from dataclasses import FrozenInstanceError
from typing import Any

import pytest

from hermes_crypto_bot.domain.exchange_capabilities import (
    CapabilityManifest,
    CapabilityRequirement,
    CapabilityViolationCode,
    EnvironmentCapabilities,
    NativeProtection,
    OrderCapabilities,
    OrderType,
    PositionMode,
    ProductCapabilities,
    TimeInForce,
    TradingEnvironment,
    TradingProduct,
    UnsupportedExchangeCapability,
    check_capabilities,
    require_capabilities,
)


def order(
    order_type: OrderType = OrderType.LIMIT,
    *,
    time_in_force: Any = frozenset({TimeInForce.GTC, TimeInForce.IOC}),
    supports_post_only: Any = True,
    supports_reduce_only: Any = True,
    native_protections: Any = frozenset({NativeProtection.STOP_LOSS}),
    position_modes: Any = frozenset({PositionMode.ONE_WAY}),
) -> OrderCapabilities:
    return OrderCapabilities(
        order_type=order_type,
        time_in_force=time_in_force,
        supports_post_only=supports_post_only,
        supports_reduce_only=supports_reduce_only,
        native_protections=native_protections,
        position_modes=position_modes,
    )


def environment(
    environment_name: TradingEnvironment = TradingEnvironment.TESTNET,
    *,
    orders: Any = None,
    candle_intervals: Any = None,
) -> EnvironmentCapabilities:
    if orders is None:
        orders = (
            order(
                OrderType.MARKET,
                time_in_force=frozenset({TimeInForce.IOC}),
                supports_post_only=False,
                supports_reduce_only=False,
                native_protections=frozenset(),
            ),
            order(OrderType.LIMIT),
            order(
                OrderType.STOP_LIMIT,
                time_in_force=frozenset({TimeInForce.IOC}),
                supports_post_only=False,
            ),
        )
    if candle_intervals is None:
        candle_intervals = frozenset({"1m", "5m", "1h"})
    return EnvironmentCapabilities(
        environment=environment_name,
        orders=orders,
        candle_intervals=candle_intervals,
    )


def futures_capabilities() -> ProductCapabilities:
    testnet = environment()
    live = environment(
        TradingEnvironment.LIVE,
        orders=(
            order(
                OrderType.MARKET,
                time_in_force=frozenset({TimeInForce.GTC}),
                supports_post_only=True,
                supports_reduce_only=True,
                native_protections=frozenset(),
                position_modes=frozenset({PositionMode.ONE_WAY}),
            ),
            order(
                OrderType.LIMIT,
                native_protections=frozenset(),
                position_modes=frozenset(),
            ),
        ),
        candle_intervals=frozenset({"1m"}),
    )
    return ProductCapabilities(
        product=TradingProduct.FUTURES,
        environments=(testnet, live),
    )


def manifest() -> CapabilityManifest:
    return CapabilityManifest(
        schema_version=1,
        exchange_code="fixture-exchange",
        products=(futures_capabilities(),),
    )


def supported_requirement() -> CapabilityRequirement:
    return CapabilityRequirement(
        environment=TradingEnvironment.TESTNET,
        product=TradingProduct.FUTURES,
        order_type=OrderType.LIMIT,
        time_in_force=TimeInForce.GTC,
        candle_interval="5m",
        post_only=True,
        native_protections=frozenset({NativeProtection.STOP_LOSS}),
        reduce_only=True,
        position_mode=PositionMode.ONE_WAY,
    )


def test_supported_requirement_passes_without_exchange_specific_branching() -> None:
    result = check_capabilities(manifest(), supported_requirement())

    assert result.supported is True
    assert result.violations == ()
    require_capabilities(manifest(), supported_requirement())


def test_manifest_and_all_profile_records_are_immutable() -> None:
    capabilities = manifest()

    with pytest.raises(FrozenInstanceError):
        capabilities.exchange_code = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        capabilities.products[0].environments[0].orders[0].supports_post_only = True  # type: ignore[misc]


def test_nested_mutable_profile_inputs_are_defensively_snapshotted() -> None:
    time_in_force = {TimeInForce.IOC}
    native_protections = {NativeProtection.STOP_LOSS}
    position_modes = {PositionMode.ONE_WAY}
    market = order(
        OrderType.MARKET,
        time_in_force=time_in_force,
        supports_post_only=False,
        supports_reduce_only=False,
        native_protections=native_protections,
        position_modes=position_modes,
    )
    orders = [market]
    candle_intervals = {"1m"}
    testnet = environment(orders=orders, candle_intervals=candle_intervals)
    environments = [testnet]
    product = ProductCapabilities(
        product=TradingProduct.FUTURES,
        environments=environments,  # type: ignore[arg-type]
    )
    products = [product]
    capabilities = CapabilityManifest(
        schema_version=1,
        exchange_code="fixture-exchange",
        products=products,  # type: ignore[arg-type]
    )

    time_in_force.add(TimeInForce.GTC)
    native_protections.clear()
    position_modes.add(PositionMode.HEDGE)
    orders.clear()
    candle_intervals.add("5m")
    environments.clear()
    products.clear()

    assert market.time_in_force == frozenset({TimeInForce.IOC})
    assert market.native_protections == frozenset({NativeProtection.STOP_LOSS})
    assert market.position_modes == frozenset({PositionMode.ONE_WAY})
    assert testnet.orders == (market,)
    assert testnet.candle_intervals == frozenset({"1m"})
    assert product.environments == (testnet,)
    assert capabilities.products == (product,)


@pytest.mark.parametrize("schema_version", [0, 2, -1, True])
def test_unknown_or_invalid_schema_versions_fail_closed(schema_version: Any) -> None:
    with pytest.raises(ValueError, match="şema sürümü"):
        CapabilityManifest(
            schema_version=schema_version,
            exchange_code="fixture-exchange",
            products=(futures_capabilities(),),
        )


@pytest.mark.parametrize(
    "exchange_code",
    ["", "BİNANCE", "binance spot", "-binance", "a" * 33, 123],
)
def test_manifest_rejects_unsafe_exchange_codes(exchange_code: Any) -> None:
    with pytest.raises(ValueError, match="Borsa kodu"):
        CapabilityManifest(
            schema_version=1,
            exchange_code=exchange_code,
            products=(futures_capabilities(),),
        )


def test_manifest_requires_at_least_one_product() -> None:
    with pytest.raises(ValueError, match="ürün yeteneği"):
        CapabilityManifest(schema_version=1, exchange_code="fixture-exchange", products=())


def test_manifest_rejects_duplicate_product_declarations() -> None:
    product = futures_capabilities()

    with pytest.raises(ValueError, match="bir kez"):
        CapabilityManifest(
            schema_version=1,
            exchange_code="fixture-exchange",
            products=(product, product),
        )


def test_product_requires_at_least_one_environment_profile() -> None:
    with pytest.raises(ValueError, match="ortam profili"):
        ProductCapabilities(product=TradingProduct.FUTURES, environments=())


def test_product_rejects_duplicate_environment_declarations() -> None:
    testnet = environment()

    with pytest.raises(ValueError, match=r"ortam.*bir kez"):
        ProductCapabilities(
            product=TradingProduct.FUTURES,
            environments=(testnet, testnet),
        )


def test_environment_requires_order_and_candle_interval() -> None:
    with pytest.raises(ValueError, match="emir yeteneği"):
        environment(orders=())
    with pytest.raises(ValueError, match="Mum zaman aralığı"):
        environment(candle_intervals=frozenset())


def test_environment_rejects_duplicate_order_declarations() -> None:
    duplicate = order()

    with pytest.raises(ValueError, match=r"emir türü.*bir kez"):
        environment(orders=(duplicate, duplicate))


def test_spot_product_cannot_claim_futures_only_semantics_in_any_profile() -> None:
    position_order = order(
        OrderType.MARKET,
        time_in_force=frozenset(),
        supports_post_only=False,
        supports_reduce_only=False,
        native_protections=frozenset(),
        position_modes=frozenset({PositionMode.ONE_WAY}),
    )
    with pytest.raises(ValueError, match=r"Spot.*pozisyon modu"):
        ProductCapabilities(
            product=TradingProduct.SPOT,
            environments=(environment(orders=(position_order,)),),
        )

    reduce_only_order = order(
        OrderType.LIMIT,
        supports_post_only=False,
        supports_reduce_only=True,
        native_protections=frozenset(),
        position_modes=frozenset(),
    )
    with pytest.raises(ValueError, match=r"Spot.*yalnız-azaltan"):
        ProductCapabilities(
            product=TradingProduct.SPOT,
            environments=(environment(orders=(reduce_only_order,)),),
        )


def test_requirement_rejects_position_mode_for_spot() -> None:
    with pytest.raises(ValueError, match=r"Spot.*pozisyon modu"):
        CapabilityRequirement(
            environment=TradingEnvironment.TESTNET,
            product=TradingProduct.SPOT,
            order_type=OrderType.MARKET,
            position_mode=PositionMode.ONE_WAY,
        )


@pytest.mark.parametrize("interval", ["", " 1m", "1 m", "1!", "../1m", "a" * 17, 1])
def test_environment_rejects_unsafe_candle_intervals(interval: Any) -> None:
    with pytest.raises(ValueError, match="Mum zaman aralığı"):
        environment(candle_intervals=frozenset({interval}))


@pytest.mark.parametrize("raw_intervals", ["1m", b"1m"])
def test_environment_rejects_scalar_text_as_candle_interval_collection(
    raw_intervals: Any,
) -> None:
    with pytest.raises(ValueError, match="koleksiyon"):
        environment(candle_intervals=raw_intervals)


def test_environment_capability_from_another_product_does_not_leak() -> None:
    spot_market = order(
        OrderType.MARKET,
        time_in_force=frozenset(),
        supports_post_only=False,
        supports_reduce_only=False,
        native_protections=frozenset(),
        position_modes=frozenset(),
    )
    spot = ProductCapabilities(
        product=TradingProduct.SPOT,
        environments=(
            environment(
                TradingEnvironment.SANDBOX,
                orders=(spot_market,),
                candle_intervals=frozenset({"15m"}),
            ),
        ),
    )
    capabilities = CapabilityManifest(
        schema_version=1,
        exchange_code="fixture-exchange",
        products=(futures_capabilities(), spot),
    )
    requirement = CapabilityRequirement(
        environment=TradingEnvironment.SANDBOX,
        product=TradingProduct.FUTURES,
        order_type=OrderType.MARKET,
        candle_interval="15m",
    )

    assert check_capabilities(capabilities, requirement).violations == (
        CapabilityViolationCode.ENVIRONMENT_UNSUPPORTED,
    )


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("order_type", "limit", "Emir türü"),
        ("time_in_force", frozenset({"gtc"}), "Emir süre türü"),
        ("time_in_force", None, "geçerli ve yinelenmeyen"),
        ("supports_post_only", 1, "Post-only"),
        ("supports_reduce_only", 0, "Yalnız-azaltan"),
        ("native_protections", frozenset({"stop_loss"}), "koruma"),
        ("position_modes", frozenset({"one_way"}), "Pozisyon modu"),
    ],
)
def test_order_rejects_malformed_adapter_fields(field: str, value: Any, message: str) -> None:
    values: dict[str, Any] = {
        "order_type": OrderType.LIMIT,
        "time_in_force": frozenset({TimeInForce.GTC}),
        "supports_post_only": True,
        "supports_reduce_only": True,
        "native_protections": frozenset({NativeProtection.STOP_LOSS}),
        "position_modes": frozenset({PositionMode.ONE_WAY}),
    }
    values[field] = value

    with pytest.raises(ValueError, match=message):
        OrderCapabilities(**values)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("environment", "testnet", "Çalışma ortamı"),
        ("orders", None, "geçerli bir koleksiyon"),
        ("orders", ("limit",), "doğrulanmış emir"),
        ("candle_intervals", None, "geçerli metin"),
    ],
)
def test_environment_rejects_malformed_adapter_fields(
    field: str,
    value: Any,
    message: str,
) -> None:
    values: dict[str, Any] = {
        "environment": TradingEnvironment.TESTNET,
        "orders": (order(),),
        "candle_intervals": frozenset({"1m"}),
    }
    values[field] = value

    with pytest.raises(ValueError, match=message):
        EnvironmentCapabilities(**values)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("product", "futures", "Ürün yalnız"),
        ("environments", None, "geçerli bir koleksiyon"),
        ("environments", ("testnet",), "doğrulanmış ortam"),
    ],
)
def test_product_rejects_malformed_adapter_fields(
    field: str,
    value: Any,
    message: str,
) -> None:
    values: dict[str, Any] = {
        "product": TradingProduct.FUTURES,
        "environments": (environment(),),
    }
    values[field] = value

    with pytest.raises(ValueError, match=message):
        ProductCapabilities(**values)


@pytest.mark.parametrize(
    ("products", "message"),
    [
        (None, "geçerli bir koleksiyon"),
        (("futures",), "doğrulanmış ürün"),
    ],
)
def test_manifest_rejects_malformed_adapter_collections(products: Any, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        CapabilityManifest(
            schema_version=1,
            exchange_code="fixture-exchange",
            products=products,
        )


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("environment", "testnet", "Çalışma ortamı"),
        ("product", "futures", "Ürün yalnız"),
        ("order_type", "market", "Emir türü"),
        ("time_in_force", "gtc", "Emir süre türü"),
        ("candle_interval", 1, "Mum zaman aralığı"),
        ("native_protections", None, "geçerli ve yinelenmeyen"),
        ("post_only", 1, "boolean"),
        ("reduce_only", 0, "boolean"),
        ("position_mode", "one_way", "Pozisyon modu"),
    ],
)
def test_requirement_rejects_malformed_typed_fields(
    field: str,
    value: Any,
    message: str,
) -> None:
    requirement = supported_requirement()
    values: dict[str, Any] = {
        "environment": requirement.environment,
        "product": requirement.product,
        "order_type": requirement.order_type,
        "time_in_force": requirement.time_in_force,
        "candle_interval": requirement.candle_interval,
        "post_only": requirement.post_only,
        "native_protections": requirement.native_protections,
        "reduce_only": requirement.reduce_only,
        "position_mode": requirement.position_mode,
    }
    values[field] = value

    with pytest.raises(ValueError, match=message):
        CapabilityRequirement(**values)


def test_testnet_only_candle_interval_is_rejected_in_live() -> None:
    requirement = CapabilityRequirement(
        environment=TradingEnvironment.LIVE,
        product=TradingProduct.FUTURES,
        order_type=OrderType.LIMIT,
        candle_interval="5m",
    )

    assert check_capabilities(manifest(), requirement).violations == (
        CapabilityViolationCode.CANDLE_INTERVAL_UNSUPPORTED,
    )


def test_testnet_limit_native_protection_and_position_mode_do_not_leak_to_live() -> None:
    requirement = CapabilityRequirement(
        environment=TradingEnvironment.LIVE,
        product=TradingProduct.FUTURES,
        order_type=OrderType.LIMIT,
        native_protections=frozenset({NativeProtection.STOP_LOSS}),
        position_mode=PositionMode.ONE_WAY,
    )

    assert check_capabilities(manifest(), requirement).violations == (
        CapabilityViolationCode.NATIVE_PROTECTION_UNSUPPORTED,
        CapabilityViolationCode.POSITION_MODE_UNSUPPORTED,
    )


def test_testnet_market_execution_features_do_not_leak_from_live_market() -> None:
    requirement = CapabilityRequirement(
        environment=TradingEnvironment.TESTNET,
        product=TradingProduct.FUTURES,
        order_type=OrderType.MARKET,
        time_in_force=TimeInForce.GTC,
        post_only=True,
        reduce_only=True,
    )

    assert check_capabilities(manifest(), requirement).violations == (
        CapabilityViolationCode.TIME_IN_FORCE_UNSUPPORTED,
        CapabilityViolationCode.POST_ONLY_UNSUPPORTED,
        CapabilityViolationCode.REDUCE_ONLY_UNSUPPORTED,
    )


def test_live_market_execution_features_are_read_from_live_market_only() -> None:
    requirement = CapabilityRequirement(
        environment=TradingEnvironment.LIVE,
        product=TradingProduct.FUTURES,
        order_type=OrderType.MARKET,
        time_in_force=TimeInForce.GTC,
        post_only=True,
        reduce_only=True,
    )

    assert check_capabilities(manifest(), requirement).supported is True


def test_order_available_only_in_another_environment_is_unsupported() -> None:
    requirement = CapabilityRequirement(
        environment=TradingEnvironment.LIVE,
        product=TradingProduct.FUTURES,
        order_type=OrderType.STOP_LIMIT,
    )

    assert check_capabilities(manifest(), requirement).violations == (
        CapabilityViolationCode.ORDER_TYPE_UNSUPPORTED,
    )


def test_undeclared_product_fails_closed_without_guessing_any_subfeature() -> None:
    requirement = CapabilityRequirement(
        environment=TradingEnvironment.SANDBOX,
        product=TradingProduct.SPOT,
        order_type=OrderType.TAKE_PROFIT_LIMIT,
        time_in_force=TimeInForce.FOK,
        candle_interval="15m",
        post_only=True,
        native_protections=frozenset({NativeProtection.TRAILING_STOP}),
        reduce_only=True,
    )

    assert check_capabilities(manifest(), requirement).violations == (
        CapabilityViolationCode.PRODUCT_UNSUPPORTED,
    )


def test_undeclared_environment_fails_closed_without_guessing_any_subfeature() -> None:
    requirement = CapabilityRequirement(
        environment=TradingEnvironment.SANDBOX,
        product=TradingProduct.FUTURES,
        order_type=OrderType.TAKE_PROFIT_LIMIT,
        time_in_force=TimeInForce.FOK,
        candle_interval="15m",
        post_only=True,
        native_protections=frozenset({NativeProtection.TRAILING_STOP}),
        reduce_only=True,
        position_mode=PositionMode.HEDGE,
    )

    assert check_capabilities(manifest(), requirement).violations == (
        CapabilityViolationCode.ENVIRONMENT_UNSUPPORTED,
    )


def test_unknown_order_does_not_guess_order_dependent_features_but_checks_candle() -> None:
    requirement = CapabilityRequirement(
        environment=TradingEnvironment.LIVE,
        product=TradingProduct.FUTURES,
        order_type=OrderType.TAKE_PROFIT_LIMIT,
        time_in_force=TimeInForce.FOK,
        candle_interval="5m",
        post_only=True,
        native_protections=frozenset({NativeProtection.TRAILING_STOP}),
        reduce_only=True,
        position_mode=PositionMode.HEDGE,
    )

    assert check_capabilities(manifest(), requirement).violations == (
        CapabilityViolationCode.ORDER_TYPE_UNSUPPORTED,
        CapabilityViolationCode.CANDLE_INTERVAL_UNSUPPORTED,
    )


def test_market_post_only_regression_is_rejected_in_its_environment_profile() -> None:
    requirement = CapabilityRequirement(
        environment=TradingEnvironment.TESTNET,
        product=TradingProduct.FUTURES,
        order_type=OrderType.MARKET,
        post_only=True,
    )

    assert check_capabilities(manifest(), requirement).violations == (
        CapabilityViolationCode.POST_ONLY_UNSUPPORTED,
    )


def test_stop_limit_gtc_regression_is_rejected_in_its_environment_profile() -> None:
    requirement = CapabilityRequirement(
        environment=TradingEnvironment.TESTNET,
        product=TradingProduct.FUTURES,
        order_type=OrderType.STOP_LIMIT,
        time_in_force=TimeInForce.GTC,
    )

    assert check_capabilities(manifest(), requirement).violations == (
        CapabilityViolationCode.TIME_IN_FORCE_UNSUPPORTED,
    )


def test_market_reduce_only_regression_is_rejected_in_its_environment_profile() -> None:
    requirement = CapabilityRequirement(
        environment=TradingEnvironment.TESTNET,
        product=TradingProduct.FUTURES,
        order_type=OrderType.MARKET,
        reduce_only=True,
    )

    assert check_capabilities(manifest(), requirement).violations == (
        CapabilityViolationCode.REDUCE_ONLY_UNSUPPORTED,
    )


def test_unsupported_order_profile_features_keep_stable_reason_codes_and_order() -> None:
    requirement = CapabilityRequirement(
        environment=TradingEnvironment.LIVE,
        product=TradingProduct.FUTURES,
        order_type=OrderType.LIMIT,
        time_in_force=TimeInForce.FOK,
        post_only=False,
        native_protections=frozenset({NativeProtection.TRAILING_STOP}),
        reduce_only=True,
        position_mode=PositionMode.HEDGE,
    )

    assert check_capabilities(manifest(), requirement).violations == (
        CapabilityViolationCode.TIME_IN_FORCE_UNSUPPORTED,
        CapabilityViolationCode.NATIVE_PROTECTION_UNSUPPORTED,
        CapabilityViolationCode.POSITION_MODE_UNSUPPORTED,
    )


def test_unsupported_capabilities_raise_a_turkish_domain_error_with_codes() -> None:
    requirement = CapabilityRequirement(
        environment=TradingEnvironment.LIVE,
        product=TradingProduct.FUTURES,
        order_type=OrderType.TAKE_PROFIT_LIMIT,
    )

    with pytest.raises(UnsupportedExchangeCapability) as error:
        require_capabilities(manifest(), requirement)

    assert error.value.violations == (CapabilityViolationCode.ORDER_TYPE_UNSUPPORTED,)
    assert "desteklemiyor" in str(error.value)
    assert "order_type_unsupported" in str(error.value)
