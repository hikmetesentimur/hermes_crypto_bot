"""Sağlayıcıdan bağımsız salt-okunur borsa metadata portu."""

import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, cast, runtime_checkable

from hermes_crypto_bot.domain.exchange_capabilities import (
    CapabilityManifest,
    OrderType,
    TradingEnvironment,
    TradingProduct,
)
from hermes_crypto_bot.domain.exchange_symbols import SymbolMetadata

_EXCHANGE_CODE_PATTERN = re.compile(r"[a-z][a-z0-9_-]{1,31}", re.ASCII)
MAX_METADATA_SNAPSHOT_RECORDS = 100_000


class MetadataViolationCode(StrEnum):
    """Adaptör metadata görüntüsündeki kararlı sözleşme ihlalleri."""

    EXCHANGE_MISMATCH = "exchange_mismatch"
    PRODUCT_UNSUPPORTED = "product_unsupported"
    ENVIRONMENT_UNSUPPORTED = "environment_unsupported"
    PRODUCT_MISMATCH = "product_mismatch"
    ENVIRONMENT_MISMATCH = "environment_mismatch"
    CAPABILITY_VERSION_MISMATCH = "capability_version_mismatch"
    SNAPSHOT_MISMATCH = "snapshot_mismatch"
    ORDER_TYPE_UNSUPPORTED = "order_type_unsupported"
    SYMBOL_DUPLICATED = "symbol_duplicated"


class MetadataContractError(ValueError):
    """Metadata görüntüsünün manifest veya istek kapsamıyla uyuşmaması."""

    def __init__(self, violations: tuple[MetadataViolationCode, ...]) -> None:
        if not violations:
            raise ValueError("En az bir metadata sözleşme ihlali gereklidir.")
        self.violations = tuple(violations)
        joined = ", ".join(item.value for item in self.violations)
        super().__init__(f"Metadata görüntüsü sözleşmeyi karşılamıyor: {joined}")


def _freeze_symbols(symbols: object) -> tuple[SymbolMetadata, ...]:
    if type(symbols) not in {list, tuple}:
        raise ValueError("Sembol metadata girdisi sonlu list veya tuple olmalıdır.")
    if len(cast(list[object] | tuple[object, ...], symbols)) > MAX_METADATA_SNAPSHOT_RECORDS:
        raise ValueError("Sembol metadata görüntüsü güvenli kayıt sınırını aşamaz.")
    snapshot: tuple[object, ...] = tuple(cast(list[object] | tuple[object, ...], symbols))
    if any(type(item) is not SymbolMetadata for item in snapshot):
        raise ValueError("Sembol metadata koleksiyonu yalnız doğrulanmış kayıtlar içermelidir.")
    return cast(tuple[SymbolMetadata, ...], snapshot)


def validate_metadata_snapshot(
    *,
    manifest: CapabilityManifest,
    environment: TradingEnvironment,
    product: TradingProduct,
    symbols: object,
) -> tuple[SymbolMetadata, ...]:
    """Metadata görüntüsünü aynı ürün/ortam yetenek profiline fail-closed bağla."""
    if type(manifest) is not CapabilityManifest:
        raise ValueError("Yetenek manifesti doğrulanmış olmalıdır.")
    if type(environment) is not TradingEnvironment:
        raise ValueError("Çalışma ortamı yalnız tanımlı değerlerden biri olmalıdır.")
    if type(product) is not TradingProduct:
        raise ValueError("Ürün yalnız tanımlı değerlerden biri olmalıdır.")

    product_profile = manifest.find_product(product)
    if product_profile is None:
        raise MetadataContractError((MetadataViolationCode.PRODUCT_UNSUPPORTED,))
    environment_profile = product_profile.find_environment(environment)
    if environment_profile is None:
        raise MetadataContractError((MetadataViolationCode.ENVIRONMENT_UNSUPPORTED,))

    snapshot = _freeze_symbols(symbols)
    supported_order_types: frozenset[OrderType] = frozenset(
        item.order_type for item in environment_profile.orders
    )
    violations: set[MetadataViolationCode] = set()
    seen_symbols: set[str] = set()

    snapshot_identities = frozenset((item.snapshot_id, item.observed_at) for item in snapshot)
    if len(snapshot_identities) > 1:
        violations.add(MetadataViolationCode.SNAPSHOT_MISMATCH)

    for item in snapshot:
        if item.exchange_symbol in seen_symbols:
            violations.add(MetadataViolationCode.SYMBOL_DUPLICATED)
        seen_symbols.add(item.exchange_symbol)

        scope_matches = True
        if item.exchange_code != manifest.exchange_code:
            violations.add(MetadataViolationCode.EXCHANGE_MISMATCH)
            scope_matches = False
        if item.product is not product:
            violations.add(MetadataViolationCode.PRODUCT_MISMATCH)
            scope_matches = False
        if item.environment is not environment:
            violations.add(MetadataViolationCode.ENVIRONMENT_MISMATCH)
            scope_matches = False
        if item.capability_schema_version != manifest.schema_version:
            violations.add(MetadataViolationCode.CAPABILITY_VERSION_MISMATCH)
            scope_matches = False
        if scope_matches and any(
            rule.order_type not in supported_order_types for rule in item.order_rules
        ):
            violations.add(MetadataViolationCode.ORDER_TYPE_UNSUPPORTED)

    if violations:
        ordered = tuple(code for code in MetadataViolationCode if code in violations)
        raise MetadataContractError(ordered)
    return snapshot


class ExchangeAdapterOperation(StrEnum):
    """Bu portta izin verilen salt-okunur adaptör operasyonları."""

    LIST_SYMBOLS = "list_symbols"
    GET_SYMBOL_METADATA = "get_symbol_metadata"


class ExchangeAdapterErrorCode(StrEnum):
    """Borsaya özgü hata metninden bağımsız normalize hata kodları."""

    RATE_LIMITED = "rate_limited"
    TIMEOUT = "timeout"
    TEMPORARILY_UNAVAILABLE = "temporarily_unavailable"
    MAINTENANCE = "maintenance"
    INVALID_RESPONSE = "invalid_response"
    UNSUPPORTED_SYMBOL = "unsupported_symbol"
    PERMISSION_DENIED = "permission_denied"


_RETRYABLE_ERRORS = frozenset(
    {
        ExchangeAdapterErrorCode.RATE_LIMITED,
        ExchangeAdapterErrorCode.TIMEOUT,
        ExchangeAdapterErrorCode.TEMPORARILY_UNAVAILABLE,
        ExchangeAdapterErrorCode.MAINTENANCE,
    }
)


@dataclass(frozen=True, slots=True, kw_only=True)
class ExchangeAdapterError(Exception):
    """Ham borsa yanıtı taşımayan normalize adaptör hatası."""

    exchange_code: str
    operation: ExchangeAdapterOperation
    code: ExchangeAdapterErrorCode

    def __post_init__(self) -> None:
        if (
            type(self.exchange_code) is not str
            or _EXCHANGE_CODE_PATTERN.fullmatch(self.exchange_code) is None
        ):
            raise ValueError("Borsa kodu güvenli küçük ASCII tanımlayıcısı olmalıdır.")
        if type(self.operation) is not ExchangeAdapterOperation:
            raise ValueError("Operasyon yalnız tanımlı değerlerden biri olmalıdır.")
        if type(self.code) is not ExchangeAdapterErrorCode:
            raise ValueError("Hata kodu yalnız tanımlı değerlerden biri olmalıdır.")

    @property
    def retryable(self) -> bool:
        """Yalnız önceden sınıflandırılmış geçici hatalarda yeniden denemeye izin ver."""
        return self.code in _RETRYABLE_ERRORS

    def __str__(self) -> str:
        return (
            f"{self.exchange_code} metadata adaptörü {self.operation.value} "
            f"işleminde {self.code.value} hatası verdi."
        )


@runtime_checkable
class ExchangeMetadataPort(Protocol):
    """Yetenek ve sembol filtreleri için salt-okunur adaptör sınırı."""

    @property
    def capabilities(self) -> CapabilityManifest:
        """Adaptörün bağlı ürün/ortam/emir yetenek manifesti."""
        ...

    async def list_symbols(
        self,
        *,
        environment: TradingEnvironment,
        product: TradingProduct,
    ) -> tuple[SymbolMetadata, ...]:
        """İstenen ürün ve ortamdaki sembol metadata görüntüsünü getir."""
        ...

    async def get_symbol_metadata(
        self,
        *,
        environment: TradingEnvironment,
        product: TradingProduct,
        exchange_symbol: str,
    ) -> SymbolMetadata:
        """İstenen tek sembolün metadata kaydını getir."""
        ...
