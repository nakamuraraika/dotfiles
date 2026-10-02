# Artifact Schema

Recommended workspace:

```text
modeling/
├── 00-frame.md
├── 01-evidence.md
├── 02-concepts.yaml
├── 03-model.md
├── 04-review.md
├── 05-decisions.md
├── 06-learning.md
├── 07-next-questions.md
├── patterns/
└── history/
    ├── n1/
    ├── n2/
    └── n3/
```

## Decision record

```yaml
id: D-001
date: YYYY-MM-DD
decision: Favoriteを独立した関係概念として扱う
status: accepted
context: 通知や履歴との関係を表現する必要がある
alternatives:
  - Userの属性として扱う
rationale: ユーザーと作品の組み合わせで識別され、独立した開始・終了を持つ
evidence: [E-003, E-008]
assumptions: []
impact: [C-User, C-Work, C-Favorite]
revisit_when: 通知以外の振る舞いを持たないことが確認された場合
```

## Learning record

```yaml
iteration: n2
new_understanding: お気に入りは評価とは独立する
invalidated_hypotheses: [H-004]
boundary_changes: []
new_unknowns: []
next_hypothesis: 通知購読はお気に入りから独立して変更可能
```
