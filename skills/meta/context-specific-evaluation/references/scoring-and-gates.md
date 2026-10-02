# Scoring and Gates

## Severity

- `CRITICAL`: invalidates the decision or creates unacceptable harm/risk.
- `HIGH`: materially threatens a primary outcome or causes expensive rework.
- `MEDIUM`: significant but bounded degradation or omission.
- `LOW`: local improvement with limited decision impact.
- `NOTE`: useful observation, not a defect.

## Confidence

- `HIGH`: directly evidenced or reproducible.
- `MEDIUM`: strong inference with limited missing evidence.
- `LOW`: plausible hypothesis requiring verification.

Do not multiply severity and confidence into a false precision score unless the domain requires it.

## Verdicts

### PASS
No unresolved critical or high issue prevents the intended decision.

### PASS_WITH_CONDITIONS
Proceed only if explicit, verifiable conditions are met.

### REVISE
The direction may be viable, but material changes are required before progression.

### BLOCK
The target or core direction is unsuitable under current goals or constraints.

### INSUFFICIENT_EVIDENCE
A responsible verdict cannot be made. State the minimum evidence needed.

## Comparison verdict

For options, state:

- recommended option;
- decisive criteria;
- trade-offs accepted;
- conditions under which another option becomes preferable;
- evidence gaps that could reverse the choice.
