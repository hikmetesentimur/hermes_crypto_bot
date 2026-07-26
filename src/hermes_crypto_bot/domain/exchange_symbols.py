"""Borsa sembol metadata ve emir türüne bağlı filtre modelleri."""

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from enum import StrEnum
from typing import Never, cast

from hermes_crypto_bot.domain.decimal_input import MAX_DECIMAL_DIGITS
from hermes_crypto_bot.domain.exchange_capabilities import (
    OrderType,
    TradingEnvironment,
    TradingProduct,
)

_EXCHANGE_CODE_PATTERN = re.compile(r"[a-z][a-z0-9_-]{1,31}", re.ASCII)
_EXCHANGE_SYMBOL_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}", re.ASCII)
_ASSET_CODE_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9._-]{0,31}", re.ASCII)
_SNAPSHOT_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}", re.ASCII)
_MAX_DECIMAL_ADJUSTED_EXPONENT = MAX_DECIMAL_DIGITS - 1


def _decimal_is_within_project_bounds(value: Decimal) -> bool:
    return (
        value.is_finite()
        and len(value.as_tuple().digits) <= MAX_DECIMAL_DIGITS
        and abs(value.adjusted()) <= _MAX_DECIMAL_ADJUSTED_EXPONENT
    )


def _require_positive_decimal(value: object, label: str) -> Decimal:
    if type(value) is not Decimal:
        raise ValueError(f"{label} Decimal olmalıdır.")
    if not value.is_finite():
        raise ValueError(f"{label} sonlu olmalıdır.")
    if value <= 0:
        raise ValueError(f"{label} pozitif olmalıdır.")
    if not _decimal_is_within_project_bounds(value):
        raise ValueError(f"{label} proje Decimal güvenli sınırları içinde olmalıdır.")
    return value


def _validate_optional_positive_decimal(value: object, label: str) -> None:
    if value is not None:
        _require_positive_decimal(value, label)


class SymbolTradingStatus(StrEnum):
    """Bir işlem çiftinin normalize edilmiş borsa durumu."""

    TRADING = "trading"
    EXIT_ONLY = "exit_only"
    SUSPENDED = "suspended"
    DELISTED = "delisted"


class NotionalFormula(StrEnum):
    """İşlem değerinin hangi açık sözleşme semantiğiyle hesaplandığı."""

    SPOT = "spot"
    LINEAR_CONTRACT = "linear_contract"
    FIXED_QUOTE_CONTRACT = "fixed_quote_contract"


class OrderPurpose(StrEnum):
    """Değer hazırlamanın yeni risk mi yoksa risk azaltımı mı olduğu."""

    ENTRY = "entry"
    EXIT = "exit"


class RoundingDirection(StrEnum):
    """Fiyat adımlama yönü; güvenli hazır değer bulunmaz."""

    DOWN = "down"
    UP = "up"


class OrderValueViolationCode(StrEnum):
    """Emir değeri hazırlama aşamasındaki kararlı güvenli-ret nedenleri."""

    SYMBOL_ENTRY_DISABLED = "symbol_entry_disabled"
    SYMBOL_EXIT_DISABLED = "symbol_exit_disabled"
    ORDER_TYPE_UNSUPPORTED = "order_type_unsupported"
    PRICE_REQUIRED = "price_required"
    PRICE_FORBIDDEN = "price_forbidden"
    PRICE_ROUNDING_REQUIRED = "price_rounding_required"
    VALUATION_PRICE_REQUIRED = "valuation_price_required"
    QUANTITY_OUTSIDE_DECIMAL_BOUNDS = "quantity_outside_decimal_bounds"
    QUANTITY_BELOW_MINIMUM = "quantity_below_minimum"
    QUANTITY_ABOVE_MAXIMUM = "quantity_above_maximum"
    PRICE_OUTSIDE_DECIMAL_BOUNDS = "price_outside_decimal_bounds"
    PRICE_BELOW_MINIMUM = "price_below_minimum"
    PRICE_ABOVE_MAXIMUM = "price_above_maximum"
    NOTIONAL_OUTSIDE_DECIMAL_BOUNDS = "notional_outside_decimal_bounds"
    NOTIONAL_BELOW_MINIMUM = "notional_below_minimum"
    NOTIONAL_ABOVE_MAXIMUM = "notional_above_maximum"


class OrderValueValidationError(ValueError):
    """Normalize edilmiş değerlerin güvenlik sınırlarını geçememesi."""

    def __init__(self, violations: tuple[OrderValueViolationCode, ...]) -> None:
        if not violations:
            raise ValueError("En az bir emir değeri ihlali gereklidir.")
        self.violations = tuple(violations)
        joined = ", ".join(item.value for item in self.violations)
        super().__init__(f"Emir değerleri güvenlik kurallarını karşılamıyor: {joined}")


@dataclass(frozen=True, slots=True, kw_only=True)
class NormalizedOrderValues:
    """Borsa adımlarına uyarlanmış ve sınırları doğrulanmış değerler."""

    quantity: Decimal
    price: Decimal | None
    notional: Decimal | None


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderSymbolRules:
    """Tek bir emir türüne bağlı fiyat, miktar ve işlem değeri filtreleri."""

    order_type: OrderType
    quantity_step: Decimal
    min_quantity: Decimal
    max_quantity: Decimal | None
    price_tick: Decimal | None
    min_price: Decimal | None
    max_price: Decimal | None
    min_notional: Decimal | None
    max_notional: Decimal | None

    def __post_init__(self) -> None:
        if type(self.order_type) is not OrderType:
            raise ValueError("Emir türü yalnız tanımlı değerlerden biri olmalıdır.")
        _require_positive_decimal(self.quantity_step, "Miktar adımı")
        _require_positive_decimal(self.min_quantity, "Asgari miktar")
        _validate_optional_positive_decimal(self.max_quantity, "Azami miktar")
        _validate_optional_positive_decimal(self.price_tick, "Fiyat adımı")
        _validate_optional_positive_decimal(self.min_price, "Asgari fiyat")
        _validate_optional_positive_decimal(self.max_price, "Azami fiyat")
        _validate_optional_positive_decimal(self.min_notional, "Asgari işlem değeri")
        _validate_optional_positive_decimal(self.max_notional, "Azami işlem değeri")

        if self.max_quantity is not None and self.max_quantity < self.min_quantity:
            raise ValueError("Azami miktar asgari miktardan küçük olamaz.")
        if (
            self.max_price is not None
            and self.min_price is not None
            and self.max_price < self.min_price
        ):
            raise ValueError("Azami fiyat asgari fiyattan küçük olamaz.")
        if (
            self.max_notional is not None
            and self.min_notional is not None
            and self.max_notional < self.min_notional
        ):
            raise ValueError("Azami işlem değeri asgari işlem değerinden küçük olamaz.")

        price_filters = (self.price_tick, self.min_price, self.max_price)
        if self.order_type is OrderType.MARKET and any(
            value is not None for value in price_filters
        ):
            raise ValueError("Market emir kuralı fiyat filtresi taşıyamaz.")
        if self.order_type is not OrderType.MARKET and self.price_tick is None:
            raise ValueError("Fiyat taşıyan emir türünde fiyat adımı zorunludur.")


@dataclass(frozen=True, slots=True, kw_only=True)
class SymbolMetadata:
    """Borsa, ürün ve ortam kimliğine bağlı değişmez sembol metadata kaydı."""

    exchange_code: str
    capability_schema_version: int
    snapshot_id: str
    observed_at: datetime
    environment: TradingEnvironment
    product: TradingProduct
    exchange_symbol: str
    base_asset: str
    quote_asset: str
    status: SymbolTradingStatus
    notional_formula: NotionalFormula
    contract_size: Decimal | None
    order_rules: tuple[OrderSymbolRules, ...]

    def __post_init__(self) -> None:
        if (
            type(self.exchange_code) is not str
            or _EXCHANGE_CODE_PATTERN.fullmatch(self.exchange_code) is None
        ):
            raise ValueError("Borsa kodu güvenli küçük ASCII tanımlayıcısı olmalıdır.")
        if type(self.capability_schema_version) is not int or self.capability_schema_version < 1:
            raise ValueError("Capability şema sürümü pozitif tam sayı olmalıdır.")
        if (
            type(self.snapshot_id) is not str
            or _SNAPSHOT_ID_PATTERN.fullmatch(self.snapshot_id) is None
        ):
            raise ValueError("Snapshot kimliği güvenli ASCII tanımlayıcısı olmalıdır.")
        if (
            type(self.observed_at) is not datetime
            or self.observed_at.tzinfo is None
            or self.observed_at.utcoffset() != timedelta(0)
        ):
            raise ValueError("Metadata gözlem zamanı UTC ve saat dilimi bilgili olmalıdır.")
        if type(self.environment) is not TradingEnvironment:
            raise ValueError("Çalışma ortamı yalnız tanımlı değerlerden biri olmalıdır.")
        if type(self.product) is not TradingProduct:
            raise ValueError("Ürün yalnız tanımlı değerlerden biri olmalıdır.")
        if (
            type(self.exchange_symbol) is not str
            or _EXCHANGE_SYMBOL_PATTERN.fullmatch(self.exchange_symbol) is None
        ):
            raise ValueError("Sembol kodu güvenli ASCII tanımlayıcısı olmalıdır.")
        for asset in (self.base_asset, self.quote_asset):
            if type(asset) is not str or _ASSET_CODE_PATTERN.fullmatch(asset) is None:
                raise ValueError("Varlık kodu güvenli büyük ASCII tanımlayıcısı olmalıdır.")
        if self.base_asset == self.quote_asset:
            raise ValueError("Baz ve karşıt varlık farklı olmalıdır.")
        if type(self.status) is not SymbolTradingStatus:
            raise ValueError("Sembol durumu yalnız tanımlı değerlerden biri olmalıdır.")
        if type(self.notional_formula) is not NotionalFormula:
            raise ValueError("Notional formülü yalnız tanımlı değerlerden biri olmalıdır.")

        if type(self.order_rules) not in {list, tuple}:
            raise ValueError("Emir kuralı koleksiyonu sonlu list veya tuple olmalıdır.")
        if len(self.order_rules) > len(OrderType):
            raise ValueError("Emir kuralları tanımlı emir türü sayısını aşamaz.")
        order_rules = tuple(self.order_rules)
        if any(type(item) is not OrderSymbolRules for item in order_rules):
            raise ValueError("Emir kuralları yalnız doğrulanmış kural kayıtları içermelidir.")
        object.__setattr__(self, "order_rules", order_rules)
        if not self.order_rules:
            raise ValueError("Her sembol en az bir emir kuralı bildirmelidir.")
        order_types = tuple(item.order_type for item in self.order_rules)
        if len(set(order_types)) != len(order_types):
            raise ValueError("Her emir türü sembolde yalnız bir kez bildirilebilir.")

        if self.product is TradingProduct.SPOT:
            if self.notional_formula is not NotionalFormula.SPOT:
                raise ValueError("Spot ürünü yalnız Spot notional formülünü kullanabilir.")
            if self.contract_size is not None:
                raise ValueError("Spot ürünü sözleşme büyüklüğü taşıyamaz.")
        else:
            if self.notional_formula not in {
                NotionalFormula.LINEAR_CONTRACT,
                NotionalFormula.FIXED_QUOTE_CONTRACT,
            }:
                raise ValueError("Vadeli ürün açık bir Vadeli notional formülü kullanmalıdır.")
            try:
                _require_positive_decimal(
                    self.contract_size,
                    "Vadeli ürün sözleşme büyüklüğü",
                )
            except ValueError as error:
                raise ValueError(
                    "Vadeli ürün sözleşme büyüklüğü pozitif, sonlu ve güvenli Decimal olmalıdır."
                ) from error

    def find_order_rules(self, order_type: OrderType) -> OrderSymbolRules | None:
        """Seçilen emir türüne bağlı filtre kaydını bul."""
        return next((item for item in self.order_rules if item.order_type is order_type), None)


def _decimal_coefficient(value: Decimal) -> tuple[int, int]:
    parts = value.as_tuple()
    coefficient = int("".join(str(digit) for digit in parts.digits))
    return coefficient, cast(int, parts.exponent)


def _decimal_from_coefficient(coefficient: int, exponent: int) -> Decimal:
    digits = tuple(int(character) for character in str(coefficient))
    return Decimal((0, digits, exponent))


def _multiply_by_integer_exact(value: Decimal, multiplier: int) -> Decimal:
    coefficient, exponent = _decimal_coefficient(value)
    return _decimal_from_coefficient(coefficient * multiplier, exponent)


def _multiply_decimals_exact(*values: Decimal) -> Decimal:
    coefficient = 1
    exponent = 0
    for value in values:
        value_coefficient, value_exponent = _decimal_coefficient(value)
        coefficient *= value_coefficient
        exponent += value_exponent
    return _decimal_from_coefficient(coefficient, exponent)


def _round_to_step(
    value: Decimal,
    step: Decimal,
    direction: RoundingDirection,
) -> Decimal:
    value_numerator, value_denominator = value.as_integer_ratio()
    step_numerator, step_denominator = step.as_integer_ratio()
    numerator = value_numerator * step_denominator
    denominator = value_denominator * step_numerator
    units, remainder = divmod(numerator, denominator)
    if direction is RoundingDirection.UP and remainder:
        units += 1
    return _multiply_by_integer_exact(step, units)


def _raise_value_violations(*violations: OrderValueViolationCode) -> Never:
    raise OrderValueValidationError(tuple(violations))


def normalize_order_values(
    *,
    metadata: SymbolMetadata,
    order_type: OrderType,
    purpose: OrderPurpose,
    quantity: Decimal,
    price: Decimal | None = None,
    price_rounding: RoundingDirection | None = None,
    valuation_price: Decimal | None = None,
) -> NormalizedOrderValues:
    """Emir değerlerini seçilen profile göre adımla ve fail-closed doğrula."""
    if type(metadata) is not SymbolMetadata:
        raise ValueError("Sembol metadata kaydı doğrulanmış olmalıdır.")
    if type(order_type) is not OrderType:
        raise ValueError("Emir türü yalnız tanımlı değerlerden biri olmalıdır.")
    if type(purpose) is not OrderPurpose:
        raise ValueError("Emir amacı yalnız tanımlı değerlerden biri olmalıdır.")
    _require_positive_decimal(quantity, "Miktar")
    if price is not None:
        _require_positive_decimal(price, "Fiyat")
    if valuation_price is not None:
        _require_positive_decimal(valuation_price, "Değerleme fiyatı")
    if price_rounding is not None and type(price_rounding) is not RoundingDirection:
        raise ValueError("Yuvarlama yönü yalnız tanımlı değerlerden biri olmalıdır.")

    if purpose is OrderPurpose.ENTRY and metadata.status is not SymbolTradingStatus.TRADING:
        _raise_value_violations(OrderValueViolationCode.SYMBOL_ENTRY_DISABLED)
    if purpose is OrderPurpose.EXIT and metadata.status not in {
        SymbolTradingStatus.TRADING,
        SymbolTradingStatus.EXIT_ONLY,
    }:
        _raise_value_violations(OrderValueViolationCode.SYMBOL_EXIT_DISABLED)

    rules = metadata.find_order_rules(order_type)
    if rules is None:
        _raise_value_violations(OrderValueViolationCode.ORDER_TYPE_UNSUPPORTED)

    normalized_quantity = _round_to_step(
        quantity,
        rules.quantity_step,
        RoundingDirection.DOWN,
    )
    violations: list[OrderValueViolationCode] = []
    if not _decimal_is_within_project_bounds(normalized_quantity):
        violations.append(OrderValueViolationCode.QUANTITY_OUTSIDE_DECIMAL_BOUNDS)
    if normalized_quantity < rules.min_quantity:
        violations.append(OrderValueViolationCode.QUANTITY_BELOW_MINIMUM)
    if rules.max_quantity is not None and normalized_quantity > rules.max_quantity:
        violations.append(OrderValueViolationCode.QUANTITY_ABOVE_MAXIMUM)

    normalized_price: Decimal | None
    if rules.price_tick is None:
        if price is not None:
            _raise_value_violations(OrderValueViolationCode.PRICE_FORBIDDEN)
        if price_rounding is not None:
            raise ValueError("Market emrinde fiyat yuvarlama yönü kullanılamaz.")
        if (
            metadata.notional_formula is NotionalFormula.FIXED_QUOTE_CONTRACT
            and valuation_price is not None
        ):
            raise ValueError("Sabit değerli sözleşmede ayrı değerleme fiyatı kullanılamaz.")
        normalized_price = None
        if (rules.min_notional is not None or rules.max_notional is not None) and (
            metadata.notional_formula is not NotionalFormula.FIXED_QUOTE_CONTRACT
            and valuation_price is None
        ):
            _raise_value_violations(OrderValueViolationCode.VALUATION_PRICE_REQUIRED)
    else:
        if valuation_price is not None:
            raise ValueError("Fiyat taşıyan emirde ayrı değerleme fiyatı kullanılamaz.")
        if price is None:
            _raise_value_violations(OrderValueViolationCode.PRICE_REQUIRED)
        if price_rounding is None:
            _raise_value_violations(OrderValueViolationCode.PRICE_ROUNDING_REQUIRED)
        normalized_price = _round_to_step(price, rules.price_tick, price_rounding)
        if not _decimal_is_within_project_bounds(normalized_price):
            violations.append(OrderValueViolationCode.PRICE_OUTSIDE_DECIMAL_BOUNDS)
        if rules.min_price is not None and normalized_price < rules.min_price:
            violations.append(OrderValueViolationCode.PRICE_BELOW_MINIMUM)
        if rules.max_price is not None and normalized_price > rules.max_price:
            violations.append(OrderValueViolationCode.PRICE_ABOVE_MAXIMUM)

    value_price = normalized_price if normalized_price is not None else valuation_price
    notional: Decimal | None = None
    if not violations:
        if metadata.notional_formula is NotionalFormula.FIXED_QUOTE_CONTRACT:
            notional = _multiply_decimals_exact(
                normalized_quantity,
                cast(Decimal, metadata.contract_size),
            )
        elif value_price is not None:
            factors = [value_price, normalized_quantity]
            if metadata.notional_formula is NotionalFormula.LINEAR_CONTRACT:
                factors.append(cast(Decimal, metadata.contract_size))
            notional = _multiply_decimals_exact(*factors)
    if notional is not None:
        if not _decimal_is_within_project_bounds(notional):
            violations.append(OrderValueViolationCode.NOTIONAL_OUTSIDE_DECIMAL_BOUNDS)
        else:
            if rules.min_notional is not None and notional < rules.min_notional:
                violations.append(OrderValueViolationCode.NOTIONAL_BELOW_MINIMUM)
            if rules.max_notional is not None and notional > rules.max_notional:
                violations.append(OrderValueViolationCode.NOTIONAL_ABOVE_MAXIMUM)

    if violations:
        raise OrderValueValidationError(tuple(violations))
    return NormalizedOrderValues(
        quantity=normalized_quantity,
        price=normalized_price,
        notional=notional,
    )
