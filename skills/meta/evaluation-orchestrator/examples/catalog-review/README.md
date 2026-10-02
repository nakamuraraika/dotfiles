# Catalog Review Example

This compact synthetic example demonstrates the decision-centered IR that motivated the Skill.

The target design derives a Work's representative Arc from the Arc with the smallest `order`. The IR does not encode “this breaks” as a fact. It separately stores:

- the observed design and stated rationale;
- invariants required for the derivation to remain valid;
- attack hypotheses such as inserting a prequel at the beginning;
- the strongest defense, including redefining `order` as representative priority;
- distinguishing tests and structural alternatives.

`evaluation-cases/CASE-PRIMARY-ARC.yaml` shows how a memorable example becomes a transition-axis case rather than a hard-coded domain anecdote.
