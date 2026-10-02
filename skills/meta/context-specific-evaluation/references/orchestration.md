# Orchestration

## When to parallelize

Use isolated reviewers when the target is consequential, complex, large, contested, or vulnerable to anchoring. Do not parallelize trivial reviews.

## Recommended roles

### Evidence and context analyst
Builds the evidence map, extracts constraints, and separates fact from inference. Does not issue the final verdict.

### Supporting reviewer
Constructs the strongest defensible case for the target, identifies valuable decisions, and states success conditions.

### Adversarial reviewer
Attempts to falsify core assumptions and find high-impact failures. Must propose remedies or verification steps.

### Coverage reviewer
Derives a concern set independently from source material and purpose, then identifies blind spots in other reviews.

### Alternative designer
Develops materially different options for disputed high-impact decisions and compares trade-offs.

### Synthesis reviewer
Receives the independent outputs after completion, resolves duplication, preserves disagreement, and produces the verdict.

## Isolation rules

- Give each reviewer the evaluation IR and relevant source pointers.
- Do not give supporting conclusions to the adversarial reviewer or vice versa.
- Require stable finding IDs or candidate IDs.
- Limit role outputs to evidence, findings, and decision consequences.
- The orchestrator must not blindly accept reviewer severity or confidence.

## Failure handling

If a reviewer fails or returns generic output:

1. record the missing perspective;
2. retry once with a narrower mandate and explicit output schema;
3. continue with reduced confidence if the perspective cannot be recovered;
4. never imply independent coverage that did not occur.
