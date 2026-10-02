# Context-Specific Evaluation Skill

A Claude Code Skill that evaluates concrete targets. It does **not** create evaluation skills.

## Responsibilities

- derive target-specific evaluation criteria;
- build a traceable evaluation IR;
- run independent supporting, adversarial, coverage, and alternative analyses;
- distinguish facts, interpretations, hypotheses, unknowns, and conflicts;
- produce prioritized findings and actionable alternatives;
- issue an explicit verdict or quality-gate decision;
- update findings efficiently across repeated review cycles.

## Install

Project scope:

```bash
mkdir -p .claude/skills
cp -R context-specific-evaluation-skill .claude/skills/context-specific-evaluation
```

User scope:

```bash
mkdir -p ~/.claude/skills
cp -R context-specific-evaluation-skill ~/.claude/skills/context-specific-evaluation
```

Optional custom subagents are included under `agents/`. To install them at project scope:

```bash
mkdir -p .claude/agents
cp context-specific-evaluation-skill/agents/*.md .claude/agents/
```

## Invocation examples

```text
この設計書を目的・制約・過去の指摘に照らして評価して。事実と仮説を分け、擁護・敵対・網羅の独立視点を統合し、優先順位付きで改善案を出して。
```

```text
候補AとBを比較評価し、採用判断、決定的な根拠、未確認事項、逆転条件を示して。
```

## Validate a workspace

```bash
python scripts/validate_workspace.py path/to/evaluation-workspace
```
