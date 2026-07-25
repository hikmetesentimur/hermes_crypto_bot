from dataclasses import FrozenInstanceError

import pytest

from hermes_crypto_bot.domain.strategy_lifecycle import (
    InvalidStrategyTransition,
    StopCompletionEvidence,
    StrategyStatus,
    transition_strategy,
)


def completed_stop_evidence() -> StopCompletionEvidence:
    return StopCompletionEvidence(
        open_trade_count=0,
        pending_protective_order_count=0,
        reconciliation_complete=True,
        partial_close_remaining=False,
    )


def test_draft_strategy_can_enter_validation() -> None:
    assert (
        transition_strategy(StrategyStatus.DRAFT, StrategyStatus.VALIDATING)
        is StrategyStatus.VALIDATING
    )


def test_strategy_uses_validated_startup_path() -> None:
    path = [
        StrategyStatus.DRAFT,
        StrategyStatus.VALIDATING,
        StrategyStatus.READY,
        StrategyStatus.STARTING,
        StrategyStatus.RUNNING,
    ]

    current = path[0]
    for target in path[1:]:
        current = transition_strategy(current, target)

    assert current is StrategyStatus.RUNNING


def test_draft_strategy_cannot_skip_validation_and_startup() -> None:
    with pytest.raises(InvalidStrategyTransition, match=r"draft.*running"):
        transition_strategy(StrategyStatus.DRAFT, StrategyStatus.RUNNING)


def test_running_strategy_can_pause_and_resume() -> None:
    paused = transition_strategy(StrategyStatus.RUNNING, StrategyStatus.PAUSED)
    resumed = transition_strategy(paused, StrategyStatus.RUNNING)

    assert resumed is StrategyStatus.RUNNING


def test_protecting_strategy_can_be_archived_only_after_proven_stop_completion() -> None:
    protecting = transition_strategy(StrategyStatus.RUNNING, StrategyStatus.PROTECTING)
    stopped = transition_strategy(
        protecting,
        StrategyStatus.STOPPED,
        stop_completion_evidence=completed_stop_evidence(),
    )
    archived = transition_strategy(stopped, StrategyStatus.ARCHIVED)

    assert archived is StrategyStatus.ARCHIVED


def test_stopping_strategy_can_stop_with_complete_and_consistent_evidence() -> None:
    stopping = transition_strategy(StrategyStatus.PAUSED, StrategyStatus.STOPPING)

    assert (
        transition_strategy(
            stopping,
            StrategyStatus.STOPPED,
            stop_completion_evidence=completed_stop_evidence(),
        )
        is StrategyStatus.STOPPED
    )


@pytest.mark.parametrize("current", [StrategyStatus.PROTECTING, StrategyStatus.STOPPING])
def test_stop_completion_evidence_is_required_before_stopped(
    current: StrategyStatus,
) -> None:
    with pytest.raises(
        InvalidStrategyTransition,
        match="durdurma tamamlanma kanıtı zorunludur",
    ):
        transition_strategy(current, StrategyStatus.STOPPED)


@pytest.mark.parametrize(
    ("evidence", "message"),
    [
        (
            StopCompletionEvidence(
                open_trade_count=1,
                pending_protective_order_count=0,
                reconciliation_complete=True,
                partial_close_remaining=False,
            ),
            "açık işlem/pozisyon",
        ),
        (
            StopCompletionEvidence(
                open_trade_count=0,
                pending_protective_order_count=1,
                reconciliation_complete=True,
                partial_close_remaining=False,
            ),
            "bekleyen koruyucu/çıkış emri",
        ),
        (
            StopCompletionEvidence(
                open_trade_count=0,
                pending_protective_order_count=0,
                reconciliation_complete=False,
                partial_close_remaining=False,
            ),
            "mutabakat tamamlanmadı",
        ),
        (
            StopCompletionEvidence(
                open_trade_count=0,
                pending_protective_order_count=0,
                reconciliation_complete=True,
                partial_close_remaining=True,
            ),
            "kısmi kapatma sürüyor",
        ),
    ],
)
@pytest.mark.parametrize("current", [StrategyStatus.PROTECTING, StrategyStatus.STOPPING])
def test_incomplete_stop_evidence_prevents_stopped(
    current: StrategyStatus,
    evidence: StopCompletionEvidence,
    message: str,
) -> None:
    with pytest.raises(InvalidStrategyTransition, match=message):
        transition_strategy(
            current,
            StrategyStatus.STOPPED,
            stop_completion_evidence=evidence,
        )


@pytest.mark.parametrize("field", ["open_trade_count", "pending_protective_order_count"])
def test_stop_completion_evidence_rejects_negative_counts(field: str) -> None:
    values: dict[str, int | bool] = {
        "open_trade_count": 0,
        "pending_protective_order_count": 0,
        "reconciliation_complete": True,
        "partial_close_remaining": False,
    }
    values[field] = -1

    with pytest.raises(ValueError, match="negatif olamaz"):
        StopCompletionEvidence(**values)  # type: ignore[arg-type]


def test_stop_completion_evidence_is_immutable() -> None:
    evidence = completed_stop_evidence()
    field = "open_trade_count"

    with pytest.raises(FrozenInstanceError):
        setattr(evidence, field, 1)


@pytest.mark.parametrize("current", [StrategyStatus.RUNNING, StrategyStatus.PAUSED])
def test_active_strategy_cannot_transition_directly_to_stopped(
    current: StrategyStatus,
) -> None:
    with pytest.raises(InvalidStrategyTransition, match=rf"{current}.*stopped"):
        transition_strategy(current, StrategyStatus.STOPPED)


def test_repeated_transition_to_current_state_is_idempotent() -> None:
    assert (
        transition_strategy(StrategyStatus.RUNNING, StrategyStatus.RUNNING)
        is StrategyStatus.RUNNING
    )


@pytest.mark.parametrize(
    "current",
    [
        StrategyStatus.VALIDATING,
        StrategyStatus.STARTING,
        StrategyStatus.RUNNING,
        StrategyStatus.PAUSED,
    ],
)
def test_operational_failure_enters_error_state(current: StrategyStatus) -> None:
    assert transition_strategy(current, StrategyStatus.ERROR) is StrategyStatus.ERROR
