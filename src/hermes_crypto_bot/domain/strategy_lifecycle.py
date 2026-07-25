"""Strateji yaşam döngüsünün güvenli durum geçişleri."""

from dataclasses import dataclass
from enum import StrEnum


class InvalidStrategyTransition(ValueError):
    """İzin verilmeyen strateji durum geçişinde oluşur."""


@dataclass(frozen=True, slots=True, kw_only=True)
class StopCompletionEvidence:
    """Stratejinin risksiz biçimde durduğunu gösteren mutabakat kanıtı."""

    open_trade_count: int
    pending_protective_order_count: int
    reconciliation_complete: bool
    partial_close_remaining: bool

    def __post_init__(self) -> None:
        if self.open_trade_count < 0:
            raise ValueError("Açık işlem/pozisyon sayısı negatif olamaz.")
        if self.pending_protective_order_count < 0:
            raise ValueError("Bekleyen koruyucu/çıkış emri sayısı negatif olamaz.")

    def require_complete(self) -> None:
        """Eksik durdurma kanıtını güvenli bir domain hatasıyla reddet."""
        if self.open_trade_count != 0:
            raise InvalidStrategyTransition("Strateji durdurulamaz: açık işlem/pozisyon bulunuyor.")
        if self.pending_protective_order_count != 0:
            raise InvalidStrategyTransition(
                "Strateji durdurulamaz: bekleyen koruyucu/çıkış emri bulunuyor."
            )
        if self.partial_close_remaining:
            raise InvalidStrategyTransition("Strateji durdurulamaz: kısmi kapatma sürüyor.")
        if not self.reconciliation_complete:
            raise InvalidStrategyTransition("Strateji durdurulamaz: mutabakat tamamlanmadı.")


class StrategyStatus(StrEnum):
    """Kalıcı strateji çalışma durumları."""

    DRAFT = "draft"
    VALIDATING = "validating"
    READY = "ready"
    STARTING = "starting"
    RUNNING = "running"
    PAUSED = "paused"
    PROTECTING = "protecting"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    ARCHIVED = "archived"


_ALLOWED_TRANSITIONS = frozenset(
    {
        (StrategyStatus.DRAFT, StrategyStatus.VALIDATING),
        (StrategyStatus.VALIDATING, StrategyStatus.READY),
        (StrategyStatus.READY, StrategyStatus.STARTING),
        (StrategyStatus.STARTING, StrategyStatus.RUNNING),
        (StrategyStatus.RUNNING, StrategyStatus.PAUSED),
        (StrategyStatus.PAUSED, StrategyStatus.RUNNING),
        (StrategyStatus.RUNNING, StrategyStatus.PROTECTING),
        (StrategyStatus.RUNNING, StrategyStatus.STOPPING),
        (StrategyStatus.PAUSED, StrategyStatus.PROTECTING),
        (StrategyStatus.PAUSED, StrategyStatus.STOPPING),
        (StrategyStatus.PROTECTING, StrategyStatus.STOPPED),
        (StrategyStatus.STOPPING, StrategyStatus.STOPPED),
        (StrategyStatus.STOPPED, StrategyStatus.ARCHIVED),
        (StrategyStatus.VALIDATING, StrategyStatus.ERROR),
        (StrategyStatus.STARTING, StrategyStatus.ERROR),
        (StrategyStatus.RUNNING, StrategyStatus.ERROR),
        (StrategyStatus.PAUSED, StrategyStatus.ERROR),
    }
)


def transition_strategy(
    current: StrategyStatus,
    target: StrategyStatus,
    *,
    stop_completion_evidence: StopCompletionEvidence | None = None,
) -> StrategyStatus:
    """Stratejiyi doğrulanmış hedef duruma geçir."""
    if current is target:
        return current
    if (
        current in {StrategyStatus.PROTECTING, StrategyStatus.STOPPING}
        and target is StrategyStatus.STOPPED
    ):
        if stop_completion_evidence is None:
            raise InvalidStrategyTransition(
                "STOPPED geçişi için durdurma tamamlanma kanıtı zorunludur."
            )
        stop_completion_evidence.require_complete()
    if (current, target) in _ALLOWED_TRANSITIONS:
        return target
    raise InvalidStrategyTransition(f"Geçersiz strateji durum geçişi: {current} -> {target}.")
