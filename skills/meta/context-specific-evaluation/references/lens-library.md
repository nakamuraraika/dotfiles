# Lens Library

Use lenses selectively. Record why a lens is relevant or skipped.

## Goal alignment
- Does the target solve the stated problem?
- Is it optimized for a proxy rather than the real outcome?

## Domain correctness
- Are concepts, invariants, terminology, and boundaries faithful to the domain?
- Does the target contradict authoritative business or technical rules?

## Completeness
- Are normal flows, edge cases, failure states, lifecycle transitions, and operational needs covered?

## Consistency
- Do claims, diagrams, interfaces, examples, and decisions agree?
- Are identical concepts represented differently without reason?

## Boundaries and responsibilities
- Is ownership clear?
- Are responsibilities cohesive and dependencies intentional?

## Feasibility and operability
- Can the target be implemented, deployed, observed, recovered, and supported under stated constraints?

## Failure and abuse
- What happens under invalid input, partial failure, concurrency, misuse, hostile behavior, and dependency failure?

## Security, privacy, compliance, safety
- Are trust boundaries, sensitive data, authorization, retention, auditability, and mandatory controls addressed?

## Performance and scale
- Are workload assumptions explicit?
- Where are bottlenecks, amplification, contention, or unbounded growth possible?

## Maintainability and evolution
- Which changes are likely?
- Does the design localize or spread those changes?
- Are irreversible commitments justified?

## Stakeholder and user impact
- Does the target create cognitive, operational, migration, accessibility, or support burden?

## Cost and reversibility
- Are implementation and ongoing costs proportional to value?
- Can the decision be safely reversed?

## Traceability and testability
- Can requirements, claims, decisions, and findings be verified?

## Reasoning quality
- Were alternatives considered?
- Are decisions proportional to evidence?
- Were contradictions and rejected options preserved?
