# Minimal Design Review Example

## Verdict

`REVISE` — the proposed boundary is directionally coherent, but ownership of lifecycle and failure recovery is unresolved, so implementation would likely spread invariants across services.

## Strength to preserve

The design correctly separates user-facing read concerns from write orchestration and explicitly records the latency goal.

## FND-001 — Lifecycle ownership is split

- Classification: INTERPRETATION
- Severity: HIGH
- Confidence: MEDIUM
- Affects: consistency, recovery, maintainability
- Evidence: component diagram and workflow description assign state creation and cancellation to different services without a named owner.

### Why it matters

Partial failure can leave state that neither service can safely reconcile.

### Recommended action

Assign a single lifecycle owner or define an explicit saga with state, compensations, idempotency, and observability.

### Verification

Walk through create, retry, timeout, cancel, and duplicate-delivery scenarios and identify the authoritative state after each step.
