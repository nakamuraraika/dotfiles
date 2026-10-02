# Evaluation Orchestration

This document defines the mandatory default execution graph for orchestrating and running an evaluation. Roles may be merged only after replay evidence shows no material loss of independent discovery, provenance, dissent, issue recall, or false-positive control.

## Canonical graph

```text
source materials
      |
      v
Source Normalizer / Reconstructor
      | source snapshot + decision-centered IR v0
      +----------------------+----------------------+
      |                      |                      |
      v                      v                      v
Adversarial Extractor   Advocate Extractor   Blind Coverage Explorer
(source + IR index)     (source + IR index)   (source only; no seeded framing)
      |                      |                      |
      +----------------------+----------------------+
                             |
                             v
                    Finding Integrator
       semantic deduplication / provenance / dissent
                             |
                             v
                  Epistemic Reclassifier
          rebuild decision records and change log
                             |
                             v
                 Evaluation Case Designer
      derive variation axes / cases / hidden holdouts
                             |
                             v
                    Evaluation Run Planner
       compile IR and visible cases into instructions
                             |
                             v
                     Final Evaluator
                             |
                             v
                    Blinded Evaluation Judge
                             |
            pass ------------------ repair or outer loop
                                      |
                                      v
                              Failure Localizer
                                      |
                                      v
                        Improvement Candidate Generator
                                      |
                                      v
                              Regression Replay
                                      |
                                      v
                         Improvement Promotion Judge
```

The improvement branch is conditional. A passing run may end after the blinded judge unless an outer-loop review was explicitly requested.

## Shared execution rules

- Primary sources are authoritative over normalized IR and all agent summaries.
- Adversarial and advocate agents must read primary sources directly and may use IR only as an index.
- Parallel paths use immutable input snapshots with no cross-agent visibility.
- A downstream stage starts only after dependencies pass structural validation.
- Every stage declares inputs, hidden inputs, outputs, assertions, retry limit, and failure route.
- Failures route to the earliest responsible stage, not merely the previous stage.

## Core stage contracts

### Source Normalizer

Produces:

- immutable source snapshot manifest;
- source-grounded evaluation IR v0;
- decision records, source items, unknowns, and missing evidence.

Must not:

- infer criticism as fact;
- optimize reconstruction around seeded concerns only;
- erase rejected alternatives or operating rules.

### Adversarial Extractor

Produces falsifiable failure hypotheses, transition cases, high-loss failure modes, structural alternatives, and distinguishing tests. It must report source discoveries absent from IR or explicitly state that none were found.

### Advocate Extractor

Produces the strongest validity conditions, defenses, required evidence, steelmanned rejected alternatives, and collapse conditions. It must also read primary sources directly.

### Blind Coverage Explorer

Sees only primary sources, immutable snapshot metadata, and the neutral evaluation purpose. It must not see source IR, seeded concerns, sibling findings, or evaluation instructions.

Produces independent dimensions, omissions, questions, section coverage, and lifecycle coverage.

### Finding Integrator

Merge only when findings share materially equivalent:

1. claim or invariant;
2. mechanism;
3. consequence;
4. evidence basis.

Preserve contrary conclusions as linked dissent. Retain source refs, origin IDs, and blind-only discovery markers.

### Epistemic Reclassifier

Rules:

- agent agreement does not promote a hypothesis to observation;
- only direct source support may justify observation;
- unverified real-world examples remain hypotheses or unknowns;
- merged statements take the least certain defensible class;
- attack, defense, and verification are linked back into decision records.

Produces IR v1 and an epistemic change log.

### Evaluation Case Designer

Derives case-generation axes from target state, transitions, ownership, lifecycle, authority, representation, environment, and recovery behavior. Produces visible cases and separately stored holdout expectations.

Every case records expected result and expected trace. Depth is risk-proportionate; arbitrary counts are forbidden.

### Evaluation Run Planner

Compiles decision records and visible cases into target-specific questions, evidence policy, execution order, severity anchors, action requirements, and a completion gate. It must not see holdout expectations.

### Final Evaluator

Executes the fixed contract. It may not silently change criteria or self-certify quality. Material claims are cited; uncertainty and dissent remain visible; material criticism includes an action, test, or structural alternative.

### Blinded Evaluation Judge

Verifies source fidelity, unsupported claims, issue recall, false positives, false negatives, independent discovery, actionability, severity calibration, and charter thresholds. It sees holdout expectations but not evaluator self-grades or current improvement proposals.

## Improvement stages

### Failure Localizer

Identifies the earliest stage that introduced the judged defect and separates root cause from downstream symptoms.

### Improvement Candidate Generator

Proposes the smallest scoped, reversible repair to the responsible component. Defines regression cases, comparison metrics, and rollback. One-off tactics remain provisional.

### Regression Replay

Replays golden, boundary, prior-failure, and holdout cases. Compares quality, cost, context growth, and human intervention and reports regressions.

### Improvement Promotion Judge

Decides to promote, retain experimentally, reject, or roll back using the promotion ladder and charter thresholds.

## Execution harness

`scripts/orchestrate.py` provides vendor-neutral state and artifact gating. It does not call an LLM itself; an agent runtime consumes the generated stage packet and writes declared outputs.

```bash
python scripts/orchestrate.py init templates/orchestration.yaml \
  --run-dir ./runs/example \
  --bind source_materials=/absolute/path/to/source

python scripts/orchestrate.py ready --run-dir ./runs/example
python scripts/orchestrate.py start source_normalizer --run-dir ./runs/example
python scripts/orchestrate.py complete source_normalizer --run-dir ./runs/example
python scripts/orchestrate.py status --run-dir ./runs/example
```

`packet` emits only allowed inputs, forbidden visibility, role contract, output paths, and assertions. `fail` applies retry budgets and earliest-stage routing. `publish` copies canonical outputs to a distribution directory.

## Completion conditions

The run is complete only when:

- required core stages have terminal success states;
- material findings have source and origin traceability;
- blind-only discoveries are reported;
- unresolved dissent is preserved;
- epistemic classification passes validation;
- evaluator instructions pass visible and holdout cases;
- judge verdict meets charter thresholds;
- retry and escalation budgets are not exceeded;
- any promoted improvement has replay evidence and rollback information.
