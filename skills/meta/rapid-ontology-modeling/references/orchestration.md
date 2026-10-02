# Orchestration

## Recommended graph

```text
Source material
 ├─ Evidence Extractor
 ├─ Concept Modeler
 ├─ Adversarial Reviewer
 └─ Alternative Modeler
          ↓
   Argument Integrator
          ↓
Fact / Interpretation / Hypothesis / Unknown separation
          ↓
   Model Synthesizer
          ↓
Quality Gate + Pattern Miner
```

## Agent contracts

### Evidence Extractor
Input: source only
Output: atomic claims, quotations/locations, evidence label, ambiguity
Forbidden: model design

### Concept Modeler
Input: frame + evidence inventory
Output: concepts, relations, constraints, minimal model, assumptions
Forbidden: hiding uncertainty

### Adversarial Reviewer
Input: frame + model
Output: counterexamples, contradictions, missing boundaries, severity
Forbidden: cosmetic comments unless they affect meaning

### Alternative Modeler
Input: frame + evidence inventory
Output: at least one materially different decomposition and trade-offs
Forbidden: merely renaming the current model

### Synthesizer
Input: all outputs
Output: merged issue map, accepted decisions, unresolved conflicts, model n+1
Forbidden: silently resolving conflicting facts

### Pattern Miner
Input: decision, learning, challenge logs
Output: provisional reusable artifacts with evidence maturity
Forbidden: generalizing from one case as a universal rule

## Context minimization

Each agent receives:

- role contract
- current frame
- required source subset
- expected output schema
- output path

Do not pass the entire conversational history unless essential. The orchestrator exchanges summaries and artifact paths.

## Retry

Retry a failed agent at most 3 times.

1. Record failure reason
2. Preserve partial artifact
3. Narrow or clarify contract
4. Re-run the same role
5. Escalate unresolved failure to the synthesis output
