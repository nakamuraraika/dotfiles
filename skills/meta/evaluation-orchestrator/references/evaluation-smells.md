# Evaluation Smells

## Generic-criteria-first
The evaluator starts with a universal checklist before understanding what failure matters in the target.

## Upstream-framing amplification
All later roles inherit one extractor's concerns and discover nothing independently.

## Interpretation laundering
An inferred premise becomes a stated fact after passing through multiple agents.

## Adversary-only distortion
The target is attacked without constructing the strongest conditions under which it succeeds.

## Toothless criticism
A criticism has no concrete failure scenario, alternative, distinguishing test, or action.

## Cosmetic alternative
The proposed alternative only renames fields or steps while preserving the same boundaries.

## Implementation witness missing
The evaluator judges conceptual elegance but not whether a practitioner can act consistently.

## Unobservable scoring
Scores have labels but no observable anchors or consequence model.

## Format-driven box filling
Mandatory sections or counts create shallow content rather than risk-proportionate depth.

## Seed-example anchoring
Provided examples dominate evaluation and suppress discovery of unrelated defects.

## Self-grading evaluator
The same process generates and certifies its own output without holdouts or independent judgment.

## Prompt patch accumulation
Every failure adds another final instruction instead of repairing the responsible upstream representation or test.

## Evaluation corpus neglect
Prompts are versioned carefully while cases, expected traces, and prior failures are not maintained.

## Shared-normalizer blindness
Adversary and advocate both inherit omissions from the same reconstruction and do not read the source independently.

## Fragmented decision evidence
Observation, rationale, attack, defense, and tests are stored as unrelated findings, forcing later agents to reconstruct their relationship.

## Declared-but-missing artifact
Documentation requires a template, validator, or example that is absent from the package.

## Validation theater
A validator succeeds by matching strings while dependencies, artifact references, contracts, or isolation constraints are structurally invalid.
