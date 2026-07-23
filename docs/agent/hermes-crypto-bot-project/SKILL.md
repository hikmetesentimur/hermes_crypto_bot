---
name: hermes-crypto-bot-project
description: Use when planning, designing, implementing, reviewing, deploying, or discussing Hikmet Esentimur's hermes_crypto_bot project. Loads the repository's source-of-truth documents, preserves decisions and traceability, enforces trading safety gates, verifies changes, and synchronizes completed artifacts to GitHub.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [project, crypto, trading, requirements, safety, github]
    related_skills: [test-driven-development, github-pr-workflow, requesting-code-review]
---

# Hermes Crypto Bot Project

## Overview

Use the Git repository as the durable project memory. Never rely on chat recollection when a repository document can establish the current requirement, decision, architecture, or safety rule.

Repository: `/opt/data/repos/hermes_crypto_bot`
Remote: `git@github.com:hikmetesentimur/hermes_crypto_bot.git`

## Start-of-Task Protocol

1. Confirm the repository exists and fetch the current remote state.
2. Read `AGENTS.md`.
3. Read `docs/README.md` and `docs/decisions/DECISION_LOG.md`.
4. Read `docs/requirements/OPEN_QUESTIONS.md` plus task-relevant requirements, architecture, security, and operations documents.
5. Check `git status` before editing.

Completion criterion: current approved decisions, unresolved blockers, and local Git state are known before proposing or changing behavior.

## Turkish Communication Protocol

1. Ask every user-facing question and present every choice in clear, plain Turkish.
2. Translate technical English terminology into Turkish. If the original English term is necessary, place it after the Turkish explanation in parentheses.
3. Do not present unexplained English jargon or abbreviations. Examples: use “emir fiyat kayması” for slippage, “sermayenin zirveden düşüşü” for drawdown, and “emir gerçekleşmesi” for fill.
4. Keep code, API, schema, and protocol identifiers in their required original form, but explain their meaning to the user in Turkish.

## Decision and Requirements Protocol

1. Preserve original user files unchanged under `docs/source/`.
2. Give every normalized requirement a stable ID and testable acceptance criteria.
3. Record unapproved ideas as proposals or open questions, never as final decisions.
4. When the user answers an open question:
   - update the question status;
   - add an entry to `docs/decisions/DECISION_LOG.md`;
   - update affected requirements and acceptance criteria;
   - add traceability links between them.
5. If a newer decision replaces an older one, retain history and mark the old decision `DEĞİŞTİRİLDİ`.

Completion criterion: every lasting user answer is represented in version-controlled project documents without erasing decision history.

## Implementation Protocol

1. Plan multi-step changes before coding.
2. Use test-driven development for calculations, risk rules, state transitions, and API contracts.
3. Keep exchange adapters and indicator plugins behind explicit interfaces.
4. Use decimal arithmetic for money, price, quantity, percentages, and PnL; never binary floats.
5. Keep simulation and live execution separated by explicit capability and safety boundaries.
6. Run targeted tests, then the full applicable quality suite.
7. Review the diff for secrets and unintended files.
8. Commit with a conventional commit message and push to GitHub.
9. Report real command/test results and the pushed branch/commit; never fabricate success.

Completion criterion: code, tests, documentation, and GitHub state agree, with actual verification output.

## Live-Trading Safety Gate

Never enable or deploy live order submission until all of these are documented, implemented, tested, and explicitly approved by the user:

- least-privilege exchange keys with withdrawal disabled;
- encrypted secret storage and rotation/revocation procedure;
- authentication, authorization, and live-mode confirmation controls;
- decimal normalization to exchange tick/step/min-notional rules;
- idempotent order intent, retry rules, timeout handling, and exchange reconciliation;
- fees, funding, slippage, partial fills, stale data, and liquidation risk handling;
- global and per-strategy exposure/loss limits;
- kill switch and safe startup/shutdown behavior;
- immutable audit log, monitoring, alerting, backups, and recovery runbooks;
- sandbox/testnet and failure-injection acceptance tests;
- explicit live activation approval after a clear risk warning and MFA; no minimum paper-performance period is required, but every technical safety check above remains mandatory.

If any item is missing, remain in simulation/test mode and record the blocker.

## Deployment Protocol

When hosting details are provided:

1. Inventory target OS, architecture, DNS, TLS, firewall, Docker/runtime, storage, database, secrets facility, backup destination, and monitoring.
2. Never paste credentials into source files, Git history, logs, or chat summaries.
3. Add reproducible deployment configuration and runbooks to the repository.
4. Deploy first with live trading disabled.
5. Verify health checks, migrations, persistence, backup/restore, restart behavior, logging, and rollback.
6. Enable external access only after TLS and authentication checks pass.

Completion criterion: a fresh operator can deploy, verify, roll back, and recover using repository instructions without exposing secrets.

## Common Pitfalls

- Treating a proposal as user approval.
- Allowing the original DOCX and normalized requirements to drift without traceability.
- Equating paper fills with live exchange fills.
- Multiplying percentage return by leverage without defining margin/notional and deducting fees/funding.
- Retrying order creation without idempotency and reconciliation.
- Using exchange API keys with withdrawal permission.
- Enabling live mode because a UI toggle changed, without server-side safety validation.
- Reporting a GitHub update before verifying the remote branch.

## Verification Checklist

- [ ] Repository and remote state inspected
- [ ] Relevant decisions and open questions loaded
- [ ] Requirements/decisions/docs updated with code
- [ ] Money calculations use decimal arithmetic
- [ ] Live-trading safety gate respected
- [ ] Tests and checks executed with real output
- [ ] Secret scan/diff review completed
- [ ] Commit created and remote push verified
