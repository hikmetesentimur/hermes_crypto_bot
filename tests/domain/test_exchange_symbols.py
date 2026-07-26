from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta, timezone
from decimal import Decimal
from typing import Any

import pytest

from hermes_crypto_bot.domain.exchange_capabilities import (
    OrderType,
    TradingEnvironment,
    TradingProduct,
)
from hermes_crypto_bot.domain.exchange_symbols import (
    NormalizedOrderValues,
    NotionalFormula,
    OrderPurpose,
    OrderSymbolRules,
    OrderValueValidationError,
    OrderValueViolationCode,
    RoundingDirection,
    SymbolMetadata,
    SymbolTradingStatus,
    normalize_order_values,
)


def limit_rules() -> OrderSymbolRules:
    return OrderSymbolRules(
        order_type=OrderType.LIMIT,
        quantity_step=Decimal("0.001"),
        min_quantity=Decimal("0.001"),
        max_quantity=Decimal("100"),
        price_tick=Decimal("0.10"),
        min_price=Decimal("0.10"),
        max_price=Decimal("1000000"),
        min_notional=Decimal("5"),
        max_notional=None,
    )


def spot_metadata() -> SymbolMetadata:
    return SymbolMetadata(
        exchange_code="fixture-exchange",
        capability_schema_version=1,
        snapshot_id="fixture-snapshot-1",
        observed_at=datetime(2026, 7, 26, 16, 0, tzinfo=UTC),
        environment=TradingEnvironment.TESTNET,
        product=TradingProduct.SPOT,
        exchange_symbol="BTCUSDT",
        base_asset="BTC",
        quote_asset="USDT",
        status=SymbolTradingStatus.TRADING,
        notional_formula=NotionalFormula.SPOT,
        contract_size=None,
        order_rules=(limit_rules(),),
    )


def test_spot_symbol_keeps_order_specific_decimal_rules() -> None:
    metadata = spot_metadata()

    assert metadata.find_order_rules(OrderType.LIMIT) == limit_rules()
    assert metadata.find_order_rules(OrderType.MARKET) is None
    assert metadata.base_asset == "BTC"
    assert metadata.quote_asset == "USDT"


def test_symbol_and_rule_records_are_immutable() -> None:
    metadata = spot_metadata()

    with pytest.raises(FrozenInstanceError):
        metadata.exchange_symbol = "CHANGED"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        metadata.order_rules[0].quantity_step = Decimal("1")  # type: ignore[misc]


def rule_values() -> dict[str, Any]:
    rules = limit_rules()
    return {
        "order_type": rules.order_type,
        "quantity_step": rules.quantity_step,
        "min_quantity": rules.min_quantity,
        "max_quantity": rules.max_quantity,
        "price_tick": rules.price_tick,
        "min_price": rules.min_price,
        "max_price": rules.max_price,
        "min_notional": rules.min_notional,
        "max_notional": rules.max_notional,
    }


def metadata_values() -> dict[str, Any]:
    metadata = spot_metadata()
    return {
        "exchange_code": metadata.exchange_code,
        "capability_schema_version": metadata.capability_schema_version,
        "snapshot_id": metadata.snapshot_id,
        "observed_at": metadata.observed_at,
        "environment": metadata.environment,
        "product": metadata.product,
        "exchange_symbol": metadata.exchange_symbol,
        "base_asset": metadata.base_asset,
        "quote_asset": metadata.quote_asset,
        "status": metadata.status,
        "notional_formula": metadata.notional_formula,
        "contract_size": metadata.contract_size,
        "order_rules": metadata.order_rules,
    }


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("order_type", "limit", "Emir türü"),
        ("quantity_step", 0.001, "Decimal"),
        ("quantity_step", Decimal("0"), "pozitif"),
        ("quantity_step", Decimal("NaN"), "sonlu"),
        ("min_quantity", Decimal("-1"), "pozitif"),
        ("max_quantity", Decimal("0.0001"), "Azami miktar"),
        ("price_tick", Decimal("Infinity"), "sonlu"),
        ("min_price", Decimal("0"), "pozitif"),
        ("max_price", Decimal("0.01"), "Azami fiyat"),
        ("min_notional", Decimal("-5"), "pozitif"),
        ("max_notional", Decimal("1"), "Azami işlem değeri"),
    ],
)
def test_order_rules_reject_malformed_or_unsafe_values(
    field: str,
    value: Any,
    message: str,
) -> None:
    values = rule_values()
    values[field] = value

    with pytest.raises(ValueError, match=message):
        OrderSymbolRules(**values)


def test_market_rule_rejects_price_filters() -> None:
    values = rule_values()
    values["order_type"] = OrderType.MARKET

    with pytest.raises(ValueError, match="Market"):
        OrderSymbolRules(**values)


def test_priced_order_requires_price_tick() -> None:
    values = rule_values()
    values["price_tick"] = None

    with pytest.raises(ValueError, match="fiyat adımı"):
        OrderSymbolRules(**values)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("exchange_code", "Binance Spot", "Borsa kodu"),
        ("capability_schema_version", True, "şema sürümü"),
        ("capability_schema_version", 0, "şema sürümü"),
        ("snapshot_id", "../snapshot", "Snapshot"),
        ("observed_at", datetime(2026, 7, 26, 16, 0), "UTC"),
        (
            "observed_at",
            datetime(2026, 7, 26, 19, 0, tzinfo=timezone(timedelta(hours=3))),
            "UTC",
        ),
        ("environment", "testnet", "Çalışma ortamı"),
        ("product", "spot", "Ürün"),
        ("exchange_symbol", "../BTCUSDT", "Sembol kodu"),
        ("base_asset", "btc", "Varlık kodu"),
        ("quote_asset", "US DT", "Varlık kodu"),
        ("status", "trading", "Sembol durumu"),
        ("order_rules", (), "emir kuralı"),
        ("order_rules", None, "koleksiyon"),
        ("order_rules", ("limit",), "doğrulanmış"),
    ],
)
def test_symbol_metadata_rejects_malformed_adapter_values(
    field: str,
    value: Any,
    message: str,
) -> None:
    values = metadata_values()
    values[field] = value

    with pytest.raises(ValueError, match=message):
        SymbolMetadata(**values)


def test_symbol_rejects_same_base_and_quote_asset() -> None:
    values = metadata_values()
    values["quote_asset"] = "BTC"

    with pytest.raises(ValueError, match="farklı"):
        SymbolMetadata(**values)


def test_symbol_rejects_duplicate_order_rule_declarations() -> None:
    values = metadata_values()
    values["order_rules"] = (limit_rules(), limit_rules())

    with pytest.raises(ValueError, match=r"emir türü.*bir kez"):
        SymbolMetadata(**values)


def test_order_rule_input_list_is_defensively_snapshotted() -> None:
    rules = [limit_rules()]
    values = metadata_values()
    values["order_rules"] = rules

    metadata = SymbolMetadata(**values)
    rules.clear()

    assert metadata.order_rules == (limit_rules(),)


def test_spot_rejects_contract_size() -> None:
    values = metadata_values()
    values["contract_size"] = Decimal("1")

    with pytest.raises(ValueError, match=r"Spot.*sözleşme"):
        SymbolMetadata(**values)


@pytest.mark.parametrize("contract_size", [None, 1, Decimal("0"), Decimal("NaN")])
def test_futures_requires_positive_finite_decimal_contract_size(contract_size: Any) -> None:
    values = metadata_values()
    values["product"] = TradingProduct.FUTURES
    values["notional_formula"] = NotionalFormula.LINEAR_CONTRACT
    values["contract_size"] = contract_size

    with pytest.raises(ValueError, match=r"Vadeli.*sözleşme"):
        SymbolMetadata(**values)


def market_rules() -> OrderSymbolRules:
    return OrderSymbolRules(
        order_type=OrderType.MARKET,
        quantity_step=Decimal("0.01"),
        min_quantity=Decimal("0.01"),
        max_quantity=Decimal("100"),
        price_tick=None,
        min_price=None,
        max_price=None,
        min_notional=Decimal("5"),
        max_notional=Decimal("100000"),
    )


def metadata_with_rules(
    *rules: OrderSymbolRules,
    status: SymbolTradingStatus = SymbolTradingStatus.TRADING,
) -> SymbolMetadata:
    values = metadata_values()
    values["order_rules"] = rules
    values["status"] = status
    return SymbolMetadata(**values)


def futures_metadata(*rules: OrderSymbolRules) -> SymbolMetadata:
    values = metadata_values()
    values["product"] = TradingProduct.FUTURES
    values["notional_formula"] = NotionalFormula.LINEAR_CONTRACT
    values["contract_size"] = Decimal("0.001")
    values["order_rules"] = rules
    return SymbolMetadata(**values)


def test_limit_values_round_quantity_down_and_price_in_explicit_direction() -> None:
    metadata = metadata_with_rules(limit_rules())

    down = normalize_order_values(
        metadata=metadata,
        order_type=OrderType.LIMIT,
        purpose=OrderPurpose.ENTRY,
        quantity=Decimal("0.0509"),
        price=Decimal("100.05"),
        price_rounding=RoundingDirection.DOWN,
    )
    up = normalize_order_values(
        metadata=metadata,
        order_type=OrderType.LIMIT,
        purpose=OrderPurpose.EXIT,
        quantity=Decimal("0.0509"),
        price=Decimal("100.05"),
        price_rounding=RoundingDirection.UP,
    )

    assert down == NormalizedOrderValues(
        quantity=Decimal("0.050"),
        price=Decimal("100.00"),
        notional=Decimal("5.00000"),
    )
    assert up == NormalizedOrderValues(
        quantity=Decimal("0.050"),
        price=Decimal("100.10"),
        notional=Decimal("5.00500"),
    )


def test_quantity_below_minimum_is_not_automatically_increased() -> None:
    metadata = metadata_with_rules(limit_rules())

    with pytest.raises(OrderValueValidationError) as captured:
        normalize_order_values(
            metadata=metadata,
            order_type=OrderType.LIMIT,
            purpose=OrderPurpose.ENTRY,
            quantity=Decimal("0.0009"),
            price=Decimal("10000"),
            price_rounding=RoundingDirection.DOWN,
        )

    assert captured.value.violations == (OrderValueViolationCode.QUANTITY_BELOW_MINIMUM,)


def test_limit_order_requires_price_and_explicit_rounding_direction() -> None:
    metadata = metadata_with_rules(limit_rules())

    with pytest.raises(OrderValueValidationError) as missing_price:
        normalize_order_values(
            metadata=metadata,
            order_type=OrderType.LIMIT,
            purpose=OrderPurpose.ENTRY,
            quantity=Decimal("1"),
        )
    assert missing_price.value.violations == (OrderValueViolationCode.PRICE_REQUIRED,)

    with pytest.raises(OrderValueValidationError) as missing_direction:
        normalize_order_values(
            metadata=metadata,
            order_type=OrderType.LIMIT,
            purpose=OrderPurpose.ENTRY,
            quantity=Decimal("1"),
            price=Decimal("100"),
        )
    assert missing_direction.value.violations == (OrderValueViolationCode.PRICE_ROUNDING_REQUIRED,)


def test_market_order_uses_explicit_valuation_price_for_notional() -> None:
    metadata = metadata_with_rules(market_rules())

    result = normalize_order_values(
        metadata=metadata,
        order_type=OrderType.MARKET,
        purpose=OrderPurpose.ENTRY,
        quantity=Decimal("0.059"),
        valuation_price=Decimal("100"),
    )

    assert result == NormalizedOrderValues(
        quantity=Decimal("0.05"),
        price=None,
        notional=Decimal("5.00"),
    )


def test_market_order_does_not_invent_or_accept_an_order_price() -> None:
    metadata = metadata_with_rules(market_rules())

    with pytest.raises(OrderValueValidationError) as missing_valuation:
        normalize_order_values(
            metadata=metadata,
            order_type=OrderType.MARKET,
            purpose=OrderPurpose.ENTRY,
            quantity=Decimal("1"),
        )
    assert missing_valuation.value.violations == (OrderValueViolationCode.VALUATION_PRICE_REQUIRED,)

    with pytest.raises(OrderValueValidationError) as unexpected_price:
        normalize_order_values(
            metadata=metadata,
            order_type=OrderType.MARKET,
            purpose=OrderPurpose.ENTRY,
            quantity=Decimal("1"),
            price=Decimal("100"),
        )
    assert unexpected_price.value.violations == (OrderValueViolationCode.PRICE_FORBIDDEN,)


def test_futures_notional_includes_contract_size() -> None:
    rules = OrderSymbolRules(
        order_type=OrderType.LIMIT,
        quantity_step=Decimal("1"),
        min_quantity=Decimal("1"),
        max_quantity=Decimal("1000"),
        price_tick=Decimal("0.1"),
        min_price=Decimal("0.1"),
        max_price=None,
        min_notional=Decimal("10"),
        max_notional=None,
    )
    metadata = futures_metadata(rules)

    result = normalize_order_values(
        metadata=metadata,
        order_type=OrderType.LIMIT,
        purpose=OrderPurpose.ENTRY,
        quantity=Decimal("2.9"),
        price=Decimal("10000.09"),
        price_rounding=RoundingDirection.DOWN,
    )

    assert result.quantity == Decimal("2")
    assert result.price == Decimal("10000.0")
    assert result.notional == Decimal("20.0000")


@pytest.mark.parametrize(
    ("status", "purpose", "violation"),
    [
        (
            SymbolTradingStatus.EXIT_ONLY,
            OrderPurpose.ENTRY,
            OrderValueViolationCode.SYMBOL_ENTRY_DISABLED,
        ),
        (
            SymbolTradingStatus.SUSPENDED,
            OrderPurpose.ENTRY,
            OrderValueViolationCode.SYMBOL_ENTRY_DISABLED,
        ),
        (
            SymbolTradingStatus.SUSPENDED,
            OrderPurpose.EXIT,
            OrderValueViolationCode.SYMBOL_EXIT_DISABLED,
        ),
        (
            SymbolTradingStatus.DELISTED,
            OrderPurpose.EXIT,
            OrderValueViolationCode.SYMBOL_EXIT_DISABLED,
        ),
    ],
)
def test_symbol_status_rejects_disallowed_order_purpose(
    status: SymbolTradingStatus,
    purpose: OrderPurpose,
    violation: OrderValueViolationCode,
) -> None:
    metadata = metadata_with_rules(limit_rules(), status=status)

    with pytest.raises(OrderValueValidationError) as captured:
        normalize_order_values(
            metadata=metadata,
            order_type=OrderType.LIMIT,
            purpose=purpose,
            quantity=Decimal("1"),
            price=Decimal("100"),
            price_rounding=RoundingDirection.DOWN,
        )

    assert captured.value.violations == (violation,)


def test_exit_only_symbol_accepts_exit_value_preparation() -> None:
    metadata = metadata_with_rules(
        limit_rules(),
        status=SymbolTradingStatus.EXIT_ONLY,
    )

    result = normalize_order_values(
        metadata=metadata,
        order_type=OrderType.LIMIT,
        purpose=OrderPurpose.EXIT,
        quantity=Decimal("1"),
        price=Decimal("100"),
        price_rounding=RoundingDirection.DOWN,
    )

    assert result.quantity == Decimal("1.000")


def test_unknown_order_type_fails_without_using_another_order_rule() -> None:
    metadata = metadata_with_rules(limit_rules())

    with pytest.raises(OrderValueValidationError) as captured:
        normalize_order_values(
            metadata=metadata,
            order_type=OrderType.MARKET,
            purpose=OrderPurpose.ENTRY,
            quantity=Decimal("1"),
            valuation_price=Decimal("100"),
        )

    assert captured.value.violations == (OrderValueViolationCode.ORDER_TYPE_UNSUPPORTED,)


@pytest.mark.parametrize(
    "value",
    [
        1,
        1.0,
        True,
        Decimal("NaN"),
        Decimal("Infinity"),
        Decimal("0"),
        Decimal("-1"),
    ],
)
def test_normalization_rejects_non_decimal_or_non_positive_quantity(value: Any) -> None:
    metadata = metadata_with_rules(limit_rules())

    with pytest.raises(ValueError, match="Miktar"):
        normalize_order_values(
            metadata=metadata,
            order_type=OrderType.LIMIT,
            purpose=OrderPurpose.ENTRY,
            quantity=value,
            price=Decimal("100"),
            price_rounding=RoundingDirection.DOWN,
        )


@pytest.mark.parametrize(
    ("purpose", "direction", "message"),
    [
        ("entry", RoundingDirection.DOWN, "Emir amacı"),
        (OrderPurpose.ENTRY, "down", "Yuvarlama yönü"),
    ],
)
def test_normalization_rejects_raw_enum_strings(
    purpose: Any,
    direction: Any,
    message: str,
) -> None:
    metadata = metadata_with_rules(limit_rules())

    with pytest.raises(ValueError, match=message):
        normalize_order_values(
            metadata=metadata,
            order_type=OrderType.LIMIT,
            purpose=purpose,
            quantity=Decimal("1"),
            price=Decimal("100"),
            price_rounding=direction,
        )


def test_value_violations_have_stable_order() -> None:
    rules = OrderSymbolRules(
        order_type=OrderType.LIMIT,
        quantity_step=Decimal("1"),
        min_quantity=Decimal("2"),
        max_quantity=Decimal("3"),
        price_tick=Decimal("1"),
        min_price=Decimal("10"),
        max_price=Decimal("20"),
        min_notional=Decimal("25"),
        max_notional=None,
    )
    metadata = metadata_with_rules(rules)

    with pytest.raises(OrderValueValidationError) as captured:
        normalize_order_values(
            metadata=metadata,
            order_type=OrderType.LIMIT,
            purpose=OrderPurpose.ENTRY,
            quantity=Decimal("1.9"),
            price=Decimal("9.9"),
            price_rounding=RoundingDirection.DOWN,
        )

    assert captured.value.violations == (
        OrderValueViolationCode.QUANTITY_BELOW_MINIMUM,
        OrderValueViolationCode.PRICE_BELOW_MINIMUM,
    )


def test_order_value_error_requires_at_least_one_violation() -> None:
    with pytest.raises(ValueError, match="En az bir"):
        OrderValueValidationError(())


@pytest.mark.parametrize("order_rules", ["limit", b"limit"])
def test_symbol_rejects_scalar_order_rule_collections(order_rules: Any) -> None:
    values = metadata_values()
    values["order_rules"] = order_rules

    with pytest.raises(ValueError, match="koleksiyon"):
        SymbolMetadata(**values)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("metadata", object(), "metadata"),
        ("order_type", "limit", "Emir türü"),
    ],
)
def test_normalization_rejects_unvalidated_identity_inputs(
    field: str,
    value: Any,
    message: str,
) -> None:
    values: dict[str, Any] = {
        "metadata": metadata_with_rules(limit_rules()),
        "order_type": OrderType.LIMIT,
        "purpose": OrderPurpose.ENTRY,
        "quantity": Decimal("1"),
        "price": Decimal("100"),
        "price_rounding": RoundingDirection.DOWN,
    }
    values[field] = value

    with pytest.raises(ValueError, match=message):
        normalize_order_values(**values)


@pytest.mark.parametrize(
    ("quantity", "price", "violation"),
    [
        (Decimal("100.001"), Decimal("100"), OrderValueViolationCode.QUANTITY_ABOVE_MAXIMUM),
        (Decimal("1"), Decimal("1000000.1"), OrderValueViolationCode.PRICE_ABOVE_MAXIMUM),
    ],
)
def test_normalization_rejects_quantity_or_price_above_maximum(
    quantity: Decimal,
    price: Decimal,
    violation: OrderValueViolationCode,
) -> None:
    with pytest.raises(OrderValueValidationError) as captured:
        normalize_order_values(
            metadata=metadata_with_rules(limit_rules()),
            order_type=OrderType.LIMIT,
            purpose=OrderPurpose.ENTRY,
            quantity=quantity,
            price=price,
            price_rounding=RoundingDirection.UP,
        )

    assert captured.value.violations == (violation,)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"price_rounding": RoundingDirection.DOWN}, "Market"),
        ({"valuation_price": Decimal("100")}, "ayrı değerleme"),
    ],
)
def test_normalization_rejects_irrelevant_price_inputs(
    kwargs: dict[str, Any],
    message: str,
) -> None:
    if "price_rounding" in kwargs:
        metadata = metadata_with_rules(market_rules())
        base: dict[str, Any] = {
            "metadata": metadata,
            "order_type": OrderType.MARKET,
            "purpose": OrderPurpose.ENTRY,
            "quantity": Decimal("1"),
            "valuation_price": Decimal("100"),
        }
    else:
        base = {
            "metadata": metadata_with_rules(limit_rules()),
            "order_type": OrderType.LIMIT,
            "purpose": OrderPurpose.ENTRY,
            "quantity": Decimal("1"),
            "price": Decimal("100"),
            "price_rounding": RoundingDirection.DOWN,
        }
    base.update(kwargs)

    with pytest.raises(ValueError, match=message):
        normalize_order_values(**base)


def test_market_without_notional_filter_does_not_require_valuation_price() -> None:
    metadata = metadata_with_rules(
        rules_without_notional := OrderSymbolRules(
            order_type=OrderType.MARKET,
            quantity_step=Decimal("0.01"),
            min_quantity=Decimal("0.01"),
            max_quantity=None,
            price_tick=None,
            min_price=None,
            max_price=None,
            min_notional=None,
            max_notional=None,
        )
    )

    result = normalize_order_values(
        metadata=metadata,
        order_type=rules_without_notional.order_type,
        purpose=OrderPurpose.ENTRY,
        quantity=Decimal("1.239"),
    )

    assert result == NormalizedOrderValues(
        quantity=Decimal("1.23"),
        price=None,
        notional=None,
    )


@pytest.mark.parametrize(
    ("min_notional", "max_notional", "valuation_price", "violation"),
    [
        (Decimal("10"), None, Decimal("5"), OrderValueViolationCode.NOTIONAL_BELOW_MINIMUM),
        (None, Decimal("4"), Decimal("5"), OrderValueViolationCode.NOTIONAL_ABOVE_MAXIMUM),
    ],
)
def test_market_notional_limits_are_enforced(
    min_notional: Decimal | None,
    max_notional: Decimal | None,
    valuation_price: Decimal,
    violation: OrderValueViolationCode,
) -> None:
    rule = OrderSymbolRules(
        order_type=OrderType.MARKET,
        quantity_step=Decimal("1"),
        min_quantity=Decimal("1"),
        max_quantity=None,
        price_tick=None,
        min_price=None,
        max_price=None,
        min_notional=min_notional,
        max_notional=max_notional,
    )

    with pytest.raises(OrderValueValidationError) as captured:
        normalize_order_values(
            metadata=metadata_with_rules(rule),
            order_type=OrderType.MARKET,
            purpose=OrderPurpose.ENTRY,
            quantity=Decimal("1"),
            valuation_price=valuation_price,
        )

    assert captured.value.violations == (violation,)


@pytest.mark.parametrize(
    "unsafe_decimal",
    [
        Decimal("1e128"),
        Decimal("1e-128"),
        Decimal("9" * 129),
    ],
)
def test_order_rules_reject_decimals_outside_safe_project_bounds(
    unsafe_decimal: Decimal,
) -> None:
    values = rule_values()
    values["quantity_step"] = unsafe_decimal

    with pytest.raises(ValueError, match="güvenli sınır"):
        OrderSymbolRules(**values)


def test_normalization_rejects_raw_decimal_outside_safe_project_bounds() -> None:
    with pytest.raises(ValueError, match="güvenli sınır"):
        normalize_order_values(
            metadata=metadata_with_rules(limit_rules()),
            order_type=OrderType.LIMIT,
            purpose=OrderPurpose.ENTRY,
            quantity=Decimal("1e128"),
            price=Decimal("100"),
            price_rounding=RoundingDirection.DOWN,
        )


def test_allowed_large_decimals_are_rounded_and_multiplied_exactly() -> None:
    rule = OrderSymbolRules(
        order_type=OrderType.LIMIT,
        quantity_step=Decimal("0.1"),
        min_quantity=Decimal("0.1"),
        max_quantity=None,
        price_tick=Decimal("0.1"),
        min_price=None,
        max_price=None,
        min_notional=None,
        max_notional=None,
    )

    result = normalize_order_values(
        metadata=metadata_with_rules(rule),
        order_type=OrderType.LIMIT,
        purpose=OrderPurpose.ENTRY,
        quantity=Decimal("12345678901234567890123456789.9"),
        price=Decimal("9876543210.1"),
        price_rounding=RoundingDirection.DOWN,
    )

    assert result.quantity == Decimal("12345678901234567890123456789.9")
    assert result.price == Decimal("9876543210.1")
    assert result.notional == Decimal("121932631126063100002606310009027587257.99")


def test_non_power_of_ten_steps_use_exact_integer_rounding() -> None:
    rule = OrderSymbolRules(
        order_type=OrderType.LIMIT,
        quantity_step=Decimal("0.03"),
        min_quantity=Decimal("0.03"),
        max_quantity=None,
        price_tick=Decimal("0.03"),
        min_price=None,
        max_price=None,
        min_notional=None,
        max_notional=None,
    )

    down = normalize_order_values(
        metadata=metadata_with_rules(rule),
        order_type=OrderType.LIMIT,
        purpose=OrderPurpose.ENTRY,
        quantity=Decimal("0.10"),
        price=Decimal("0.10"),
        price_rounding=RoundingDirection.DOWN,
    )
    up = normalize_order_values(
        metadata=metadata_with_rules(rule),
        order_type=OrderType.LIMIT,
        purpose=OrderPurpose.EXIT,
        quantity=Decimal("0.10"),
        price=Decimal("0.10"),
        price_rounding=RoundingDirection.UP,
    )

    assert down.quantity == Decimal("0.09")
    assert down.price == Decimal("0.09")
    assert up.quantity == Decimal("0.09")
    assert up.price == Decimal("0.12")


def test_symbol_rejects_raw_or_product_incompatible_notional_formula() -> None:
    values = metadata_values()
    values["notional_formula"] = "spot"
    with pytest.raises(ValueError, match="Notional formülü"):
        SymbolMetadata(**values)

    values = metadata_values()
    values["notional_formula"] = NotionalFormula.LINEAR_CONTRACT
    with pytest.raises(ValueError, match=r"Spot.*notional"):
        SymbolMetadata(**values)

    values = metadata_values()
    values["product"] = TradingProduct.FUTURES
    values["notional_formula"] = NotionalFormula.SPOT
    values["contract_size"] = Decimal("1")
    with pytest.raises(ValueError, match=r"Vadeli.*notional"):
        SymbolMetadata(**values)


def test_fixed_quote_contract_notional_does_not_require_or_use_price() -> None:
    rule = OrderSymbolRules(
        order_type=OrderType.MARKET,
        quantity_step=Decimal("1"),
        min_quantity=Decimal("1"),
        max_quantity=None,
        price_tick=None,
        min_price=None,
        max_price=None,
        min_notional=Decimal("10"),
        max_notional=None,
    )
    values = metadata_values()
    values["product"] = TradingProduct.FUTURES
    values["notional_formula"] = NotionalFormula.FIXED_QUOTE_CONTRACT
    values["contract_size"] = Decimal("5")
    values["order_rules"] = (rule,)
    metadata = SymbolMetadata(**values)

    result = normalize_order_values(
        metadata=metadata,
        order_type=OrderType.MARKET,
        purpose=OrderPurpose.ENTRY,
        quantity=Decimal("2.9"),
    )

    assert result == NormalizedOrderValues(
        quantity=Decimal("2"),
        price=None,
        notional=Decimal("10"),
    )

    with pytest.raises(ValueError, match="değerleme fiyatı"):
        normalize_order_values(
            metadata=metadata,
            order_type=OrderType.MARKET,
            purpose=OrderPurpose.ENTRY,
            quantity=Decimal("2"),
            valuation_price=Decimal("100"),
        )


def test_symbol_rejects_order_rule_generator_without_consuming_it() -> None:
    def unsafe_generator():
        raise AssertionError("generator must not be consumed")
        yield limit_rules()

    values = metadata_values()
    values["order_rules"] = unsafe_generator()

    with pytest.raises(ValueError, match="list veya tuple"):
        SymbolMetadata(**values)


@pytest.mark.parametrize(
    ("quantity", "quantity_step", "price", "price_tick", "direction", "violation"),
    [
        (
            Decimal("9e127"),
            Decimal("3e-127"),
            Decimal("1"),
            Decimal("1"),
            RoundingDirection.DOWN,
            OrderValueViolationCode.QUANTITY_OUTSIDE_DECIMAL_BOUNDS,
        ),
        (
            Decimal("1"),
            Decimal("1"),
            Decimal("9e127"),
            Decimal("6e127"),
            RoundingDirection.UP,
            OrderValueViolationCode.PRICE_OUTSIDE_DECIMAL_BOUNDS,
        ),
    ],
)
def test_derived_step_result_outside_decimal_bounds_is_rejected(
    quantity: Decimal,
    quantity_step: Decimal,
    price: Decimal,
    price_tick: Decimal,
    direction: RoundingDirection,
    violation: OrderValueViolationCode,
) -> None:
    rule = OrderSymbolRules(
        order_type=OrderType.LIMIT,
        quantity_step=quantity_step,
        min_quantity=quantity_step,
        max_quantity=None,
        price_tick=price_tick,
        min_price=None,
        max_price=None,
        min_notional=None,
        max_notional=None,
    )

    with pytest.raises(OrderValueValidationError) as captured:
        normalize_order_values(
            metadata=metadata_with_rules(rule),
            order_type=OrderType.LIMIT,
            purpose=OrderPurpose.ENTRY,
            quantity=quantity,
            price=price,
            price_rounding=direction,
        )

    assert violation in captured.value.violations


def test_derived_notional_outside_decimal_bounds_is_rejected() -> None:
    rule = OrderSymbolRules(
        order_type=OrderType.LIMIT,
        quantity_step=Decimal("1"),
        min_quantity=Decimal("1"),
        max_quantity=None,
        price_tick=Decimal("1"),
        min_price=None,
        max_price=None,
        min_notional=None,
        max_notional=None,
    )

    with pytest.raises(OrderValueValidationError) as captured:
        normalize_order_values(
            metadata=metadata_with_rules(rule),
            order_type=OrderType.LIMIT,
            purpose=OrderPurpose.ENTRY,
            quantity=Decimal("9e127"),
            price=Decimal("9e127"),
            price_rounding=RoundingDirection.DOWN,
        )

    assert captured.value.violations == (OrderValueViolationCode.NOTIONAL_OUTSIDE_DECIMAL_BOUNDS,)


def test_symbol_rejects_more_rules_than_defined_order_types() -> None:
    values = metadata_values()
    values["order_rules"] = [limit_rules()] * (len(OrderType) + 1)

    with pytest.raises(ValueError, match="emir türü sayısını"):
        SymbolMetadata(**values)
