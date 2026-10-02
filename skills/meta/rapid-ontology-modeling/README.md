# Rapid Ontology Modeling Skill

Claude Code向けの、超高速フィードバックループ型オントロジー化・モデリングSkillです。

## Installation

プロジェクト単位:

```bash
mkdir -p .claude/skills
cp -R rapid-ontology-modeling .claude/skills/
```

ユーザー共通:

```bash
mkdir -p ~/.claude/skills
cp -R rapid-ontology-modeling ~/.claude/skills/
```

## Example requests

- このヒアリング結果をオントロジー化して
- 業務概念と境界を抽出し、モデルn1を作って
- 現在のドメインモデルを反証レビューして
- モデルの差分、判断理由、未解決点を整理して
- このモデリング過程から再利用パターンを抽出して

## Contents

- `SKILL.md`: オーケストレーションと実行規約
- `references/`: 抽出、品質評価、反証、パターン化、並列実行
- `templates/`: モデルワークスペースとパターンカード
- `examples/`: 最小実例
- `scripts/`: 成果物の簡易検証
