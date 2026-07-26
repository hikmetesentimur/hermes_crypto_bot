"""Borsa adaptörlerinin sürümlü ve güvenli yetenek sözleşmesi."""

import re
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum, StrEnum

_SUPPORTED_SCHEMA_VERSION = 1
_EXCHANGE_CODE_PATTERN = re.compile(r"[a-z][a-z0-9_-]{1,31}", re.ASCII)
_CAPABILITY_TOKEN_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,15}", re.ASCII)


def _freeze_enum_set[EnumT: Enum](
    values: Iterable[EnumT],
    enum_type: type[EnumT],
    label: str,
) -> frozenset[EnumT]:
    """Adaptör koleksiyonunu kopyala ve ham metin/değer sızıntısını reddet."""
    try:
        frozen = frozenset(values)
    except TypeError as error:
        raise ValueError(f"{label} geçerli ve yinelenmeyen değerlerden oluşmalıdır.") from error
    if any(type(value) is not enum_type for value in frozen):
        raise ValueError(f"{label} yalnız tanımlı enum değerlerini içermelidir.")
    return frozen


def _freeze_capability_tokens(values: Iterable[str], label: str) -> frozenset[str]:
    """Borsaya özgü güvenli tanımlayıcıları değişmez kopyaya dönüştür."""
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{label} tekil metin değil, bir tanımlayıcı koleksiyonu olmalıdır.")
    try:
        frozen = frozenset(values)
    except TypeError as error:
        raise ValueError(f"{label} geçerli metin değerlerinden oluşmalıdır.") from error
    if any(
        type(value) is not str or _CAPABILITY_TOKEN_PATTERN.fullmatch(value) is None
        for value in frozen
    ):
        raise ValueError(
            f"{label} 1-16 karakter uzunluğunda güvenli ASCII tanımlayıcıları içermelidir."
        )
    return frozen


class TradingProduct(StrEnum):
    """Borsada işlem yapılabilen ürün sınıfı."""

    SPOT = "spot"
    FUTURES = "futures"


class TradingEnvironment(StrEnum):
    """Adaptörün bağlanabildiği borsa ortamı."""

    SANDBOX = "sandbox"
    TESTNET = "testnet"
    LIVE = "live"


class OrderType(StrEnum):
    """Borsa tarafından yerel olarak yürütülebilen emir türü."""

    MARKET = "market"
    LIMIT = "limit"
    STOP_LIMIT = "stop_limit"
    TAKE_PROFIT_LIMIT = "take_profit_limit"


class TimeInForce(StrEnum):
    """Emrin borsadaki geçerlilik süresi türü."""

    GTC = "gtc"
    IOC = "ioc"
    FOK = "fok"
    GTD = "gtd"


class NativeProtection(StrEnum):
    """Borsanın kendi altyapısında tutabildiği koruma türü."""

    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"
    TRAILING_STOP = "trailing_stop"


class PositionMode(StrEnum):
    """Vadeli işlem pozisyon sahipliği biçimi."""

    ONE_WAY = "one_way"
    HEDGE = "hedge"


class CapabilityViolationCode(StrEnum):
    """Yetenek uyuşmazlıkları için kararlı makine kodları."""

    ENVIRONMENT_UNSUPPORTED = "environment_unsupported"
    PRODUCT_UNSUPPORTED = "product_unsupported"
    ORDER_TYPE_UNSUPPORTED = "order_type_unsupported"
    TIME_IN_FORCE_UNSUPPORTED = "time_in_force_unsupported"
    CANDLE_INTERVAL_UNSUPPORTED = "candle_interval_unsupported"
    POST_ONLY_UNSUPPORTED = "post_only_unsupported"
    NATIVE_PROTECTION_UNSUPPORTED = "native_protection_unsupported"
    REDUCE_ONLY_UNSUPPORTED = "reduce_only_unsupported"
    POSITION_MODE_UNSUPPORTED = "position_mode_unsupported"


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderCapabilities:
    """Tek bir emir türünün değişmez yürütme yetenekleri."""

    order_type: OrderType
    time_in_force: frozenset[TimeInForce]
    supports_post_only: bool
    supports_reduce_only: bool
    native_protections: frozenset[NativeProtection]
    position_modes: frozenset[PositionMode]

    def __post_init__(self) -> None:
        if type(self.order_type) is not OrderType:
            raise ValueError("Emir türü yalnız tanımlı değerlerden biri olmalıdır.")
        object.__setattr__(
            self,
            "time_in_force",
            _freeze_enum_set(self.time_in_force, TimeInForce, "Emir süre türü bildirimi"),
        )
        if type(self.supports_post_only) is not bool:
            raise ValueError("Post-only yetenek bildirimi boolean olmalıdır.")
        if type(self.supports_reduce_only) is not bool:
            raise ValueError("Yalnız-azaltan yetenek bildirimi boolean olmalıdır.")
        object.__setattr__(
            self,
            "native_protections",
            _freeze_enum_set(
                self.native_protections,
                NativeProtection,
                "Borsa-yerel koruma bildirimi",
            ),
        )
        object.__setattr__(
            self,
            "position_modes",
            _freeze_enum_set(self.position_modes, PositionMode, "Pozisyon modu bildirimi"),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class EnvironmentCapabilities:
    """Tek bir çalışma ortamının bağlı veri ve emir profilleri."""

    environment: TradingEnvironment
    orders: tuple[OrderCapabilities, ...]
    candle_intervals: frozenset[str]

    def __post_init__(self) -> None:
        if type(self.environment) is not TradingEnvironment:
            raise ValueError("Çalışma ortamı yalnız tanımlı değerlerden biri olmalıdır.")
        try:
            orders = tuple(self.orders)
        except TypeError as error:
            raise ValueError("Emir yetenekleri geçerli bir koleksiyon olmalıdır.") from error
        if any(type(order) is not OrderCapabilities for order in orders):
            raise ValueError("Emir yetenekleri yalnız doğrulanmış emir bildirimleri içermelidir.")
        object.__setattr__(self, "orders", orders)
        object.__setattr__(
            self,
            "candle_intervals",
            _freeze_capability_tokens(self.candle_intervals, "Mum zaman aralığı bildirimi"),
        )
        if not self.orders:
            raise ValueError("Her ortam en az bir emir yeteneği bildirmelidir.")
        if not self.candle_intervals:
            raise ValueError("Her ortam en az bir Mum zaman aralığı bildirmelidir.")
        order_types = tuple(item.order_type for item in self.orders)
        if len(set(order_types)) != len(order_types):
            raise ValueError("Her emir türü ortam içinde yalnız bir kez bildirilebilir.")

    def find_order(self, order_type: OrderType) -> OrderCapabilities | None:
        """İstenen emir türünün bu ortama bağlı profilini bul."""
        return next((item for item in self.orders if item.order_type is order_type), None)


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductCapabilities:
    """Bir ürünün birbirinden yalıtılmış çalışma ortamı profilleri."""

    product: TradingProduct
    environments: tuple[EnvironmentCapabilities, ...]

    def __post_init__(self) -> None:
        if type(self.product) is not TradingProduct:
            raise ValueError("Ürün yalnız tanımlı işlem ürünü değerlerinden biri olmalıdır.")
        try:
            environments = tuple(self.environments)
        except TypeError as error:
            raise ValueError("Ortam yetenekleri geçerli bir koleksiyon olmalıdır.") from error
        if any(type(item) is not EnvironmentCapabilities for item in environments):
            raise ValueError("Ortam yetenekleri yalnız doğrulanmış ortam bildirimleri içermelidir.")
        object.__setattr__(self, "environments", environments)
        if not self.environments:
            raise ValueError("Her ürün en az bir ortam profili bildirmelidir.")
        environment_names = tuple(item.environment for item in self.environments)
        if len(set(environment_names)) != len(environment_names):
            raise ValueError("Her ortam ürün içinde yalnız bir kez bildirilebilir.")
        orders = tuple(order for item in self.environments for order in item.orders)
        if self.product is TradingProduct.SPOT and any(order.position_modes for order in orders):
            raise ValueError("Spot ürünü vadeli işlem pozisyon modu bildiremez.")
        if self.product is TradingProduct.SPOT and any(
            order.supports_reduce_only for order in orders
        ):
            raise ValueError("Spot ürünü yalnız-azaltan vadeli emir yeteneği bildiremez.")

    def find_environment(
        self,
        environment: TradingEnvironment,
    ) -> EnvironmentCapabilities | None:
        """İstenen çalışma ortamının bu ürüne bağlı profilini bul."""
        return next((item for item in self.environments if item.environment is environment), None)


@dataclass(frozen=True, slots=True, kw_only=True)
class CapabilityManifest:
    """Bir borsa adaptörünün sürümlü ve değişmez ürün matrisi."""

    schema_version: int
    exchange_code: str
    products: tuple[ProductCapabilities, ...]

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int or self.schema_version != _SUPPORTED_SCHEMA_VERSION:
            raise ValueError(f"Desteklenmeyen borsa yetenek şema sürümü: {self.schema_version}.")
        if (
            type(self.exchange_code) is not str
            or _EXCHANGE_CODE_PATTERN.fullmatch(self.exchange_code) is None
        ):
            raise ValueError(
                "Borsa kodu 2-32 karakter uzunluğunda, küçük ASCII harf ile başlayan "
                "ve yalnız küçük harf, rakam, '_' veya '-' içeren bir değer olmalıdır."
            )
        try:
            products = tuple(self.products)
        except TypeError as error:
            raise ValueError("Ürün yetenekleri geçerli bir koleksiyon olmalıdır.") from error
        if any(type(product) is not ProductCapabilities for product in products):
            raise ValueError("Ürün yetenekleri yalnız doğrulanmış ürün bildirimleri içermelidir.")
        object.__setattr__(self, "products", products)
        if not self.products:
            raise ValueError("En az bir ürün yeteneği bildirilmelidir.")
        product_names = tuple(item.product for item in self.products)
        if len(set(product_names)) != len(product_names):
            raise ValueError("Her ürün yeteneği manifestte yalnız bir kez bildirilebilir.")

    def find_product(self, product: TradingProduct) -> ProductCapabilities | None:
        """İstenen ürünü borsaya özel koşul yazmadan bul."""
        return next((item for item in self.products if item.product is product), None)


@dataclass(frozen=True, slots=True, kw_only=True)
class CapabilityRequirement:
    """Bir strateji veya emrin adaptörden beklediği yürütme yetenekleri."""

    environment: TradingEnvironment
    product: TradingProduct
    order_type: OrderType
    time_in_force: TimeInForce | None = None
    candle_interval: str | None = None
    post_only: bool = False
    native_protections: frozenset[NativeProtection] = frozenset()
    reduce_only: bool = False
    position_mode: PositionMode | None = None

    def __post_init__(self) -> None:
        if type(self.environment) is not TradingEnvironment:
            raise ValueError("Çalışma ortamı yalnız tanımlı değerlerden biri olmalıdır.")
        if type(self.product) is not TradingProduct:
            raise ValueError("Ürün yalnız tanımlı işlem ürünü değerlerinden biri olmalıdır.")
        if type(self.order_type) is not OrderType:
            raise ValueError("Emir türü yalnız tanımlı değerlerden biri olmalıdır.")
        if self.time_in_force is not None and type(self.time_in_force) is not TimeInForce:
            raise ValueError("Emir süre türü yalnız tanımlı değerlerden biri olmalıdır.")
        if self.candle_interval is not None:
            interval = _freeze_capability_tokens(
                (self.candle_interval,),
                "Mum zaman aralığı gereksinimi",
            )
            object.__setattr__(self, "candle_interval", next(iter(interval)))
        object.__setattr__(
            self,
            "native_protections",
            _freeze_enum_set(
                self.native_protections,
                NativeProtection,
                "Borsa-yerel koruma gereksinimi",
            ),
        )
        if type(self.post_only) is not bool or type(self.reduce_only) is not bool:
            raise ValueError("Post-only ve yalnız-azaltan gereksinimleri boolean olmalıdır.")
        if self.position_mode is not None and type(self.position_mode) is not PositionMode:
            raise ValueError("Pozisyon modu yalnız tanımlı değerlerden biri olmalıdır.")
        if self.product is TradingProduct.SPOT and self.position_mode is not None:
            raise ValueError("Spot ürünü için vadeli işlem pozisyon modu istenemez.")


@dataclass(frozen=True, slots=True, kw_only=True)
class CapabilityCheckResult:
    """Yetenek kontrolünün açıklanabilir ve değişmez sonucu."""

    violations: tuple[CapabilityViolationCode, ...]

    @property
    def supported(self) -> bool:
        """Bütün istenen yeteneklerin bildirildiğini göster."""
        return not self.violations


class UnsupportedExchangeCapability(ValueError):
    """Adaptör istenen yeteneklerin tamamını güvenle sunamadığında oluşur."""

    def __init__(self, violations: tuple[CapabilityViolationCode, ...]) -> None:
        self.violations = violations
        codes = ", ".join(code.value for code in violations)
        super().__init__(f"Seçilen borsa/ürün istenen yetenekleri desteklemiyor: {codes}.")


def check_capabilities(
    manifest: CapabilityManifest,
    requirement: CapabilityRequirement,
) -> CapabilityCheckResult:
    """Bağlı ürün/ortam/emir matrisini fail-closed olarak denetle."""
    violations: list[CapabilityViolationCode] = []

    product = manifest.find_product(requirement.product)
    if product is None:
        return CapabilityCheckResult(violations=(CapabilityViolationCode.PRODUCT_UNSUPPORTED,))

    environment = product.find_environment(requirement.environment)
    if environment is None:
        return CapabilityCheckResult(violations=(CapabilityViolationCode.ENVIRONMENT_UNSUPPORTED,))

    selected_order = environment.find_order(requirement.order_type)
    if selected_order is None:
        violations.append(CapabilityViolationCode.ORDER_TYPE_UNSUPPORTED)
    elif (
        requirement.time_in_force is not None
        and requirement.time_in_force not in selected_order.time_in_force
    ):
        violations.append(CapabilityViolationCode.TIME_IN_FORCE_UNSUPPORTED)

    if (
        requirement.candle_interval is not None
        and requirement.candle_interval not in environment.candle_intervals
    ):
        violations.append(CapabilityViolationCode.CANDLE_INTERVAL_UNSUPPORTED)
    if (
        selected_order is not None
        and requirement.post_only
        and not selected_order.supports_post_only
    ):
        violations.append(CapabilityViolationCode.POST_ONLY_UNSUPPORTED)
    if selected_order is not None and not requirement.native_protections.issubset(
        selected_order.native_protections
    ):
        violations.append(CapabilityViolationCode.NATIVE_PROTECTION_UNSUPPORTED)
    if (
        selected_order is not None
        and requirement.reduce_only
        and not selected_order.supports_reduce_only
    ):
        violations.append(CapabilityViolationCode.REDUCE_ONLY_UNSUPPORTED)
    if (
        selected_order is not None
        and requirement.position_mode is not None
        and requirement.position_mode not in selected_order.position_modes
    ):
        violations.append(CapabilityViolationCode.POSITION_MODE_UNSUPPORTED)

    return CapabilityCheckResult(violations=tuple(violations))


def require_capabilities(
    manifest: CapabilityManifest,
    requirement: CapabilityRequirement,
) -> None:
    """Eksik borsa yeteneğinde açık alan hatası üret."""
    result = check_capabilities(manifest, requirement)
    if not result.supported:
        raise UnsupportedExchangeCapability(result.violations)
