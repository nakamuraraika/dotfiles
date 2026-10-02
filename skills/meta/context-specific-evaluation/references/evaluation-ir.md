# Evaluation IR

The evaluation IR is a compact executable representation of the review problem. It should preserve decision-relevant context while removing narrative noise.

## Required fields

- target identity and version;
- intended outcomes;
- decisions supported;
- stakeholders;
- domain concepts and boundaries;
- requirements and constraints;
- target claims;
- assumptions and dependencies;
- examples and counterexamples;
- prior decisions and feedback;
- evidence map;
- open questions and conflicts;
- selected lenses and rationale;
- preliminary success and failure conditions.

## Quality checks

- Every criterion links to a goal, constraint, or stakeholder concern.
- Every assumption has an owner or verification path where possible.
- Evidence and interpretation are not merged.
- Prior feedback is preserved without automatically treating it as correct.
- The IR is sufficient for an independent reviewer to execute the review.
