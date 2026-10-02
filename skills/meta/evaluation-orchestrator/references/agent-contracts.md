# Agent Contracts

The executable contract registry is `templates/agent-contracts.yaml`. This document explains the shared rules.

## Primary-source supremacy

The source is authoritative over every upstream summary. Adversarial and advocate agents may use `source_ir_v0` as an index, but must read primary sources directly and must report whether they found source material absent from the IR.

## Output discipline

Every stage emits only its declared artifacts. Findings use `templates/finding.yaml`; target reconstruction and reclassification use the decision-centered `templates/evaluation-ir.yaml`.

## Independence

A role is independent only when its input packet omits forbidden information. Role names do not create independence. The blind explorer must never receive seeded concerns, IR interpretations, or sibling findings.

## Epistemic discipline

Agent agreement is not evidence of truth. Only direct source support can justify `observation`. Unverified real-world examples remain hypotheses or unknowns.

## Actionability

Material criticism must include a concrete failure scenario, falsifying observation, structural alternative, distinguishing test, or repair and verification path.

## Failure reporting

A stage must fail explicitly when its success assertions are not met. It must not fill missing evidence with plausible prose merely to satisfy a schema.
