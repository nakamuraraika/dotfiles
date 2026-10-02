# Pattern System

## Mining pipeline

1. Candidate extraction
2. Context removal
3. Invariant identification
4. Applicability and non-applicability definition
5. Counterexample search
6. Existing pattern comparison
7. Evidence scoring
8. Library registration or provisional storage

## Pattern types

- Structural pattern
- Boundary pattern
- Lifecycle pattern
- State pattern
- Ownership pattern
- Rule pattern
- Vocabulary pattern
- Review pattern
- Question pattern
- Process pattern

## Canonical pattern card

```yaml
id: P-001
name: Lifecycle Split
status: provisional
problem: 単一概念に異なる生成・変更・終了規則が混在する
context: 同じ名称で扱われる情報群
forces:
  - 一貫性
  - 独立変更
  - 説明容易性
solution: ライフサイクル単位で概念または境界を分割する
applicable_when: [所有者または終了条件が異なる]
not_applicable_when: [差が表示上だけで業務上の独立性がない]
consequences:
  positive: []
  negative: []
detection_signals: []
counterexamples: []
related_patterns: []
related_antipatterns: []
evidence:
  occurrences: 1
  domains: [anime-sns]
  confidence: low
```

## Anti-pattern card

```yaml
id: AP-001
name: Mixed Abstraction View
symptoms: [業務概念とDB・UI要素が同列に並ぶ]
root_cause: モデル目的と抽象度が固定されていない
harm: 境界と責任の議論ができない
detection: 各要素に抽象度ラベルを付ける
prevention: ビューごとに抽象度を固定する
recovery: 実装要素を別ビューへ移す
```

## Question card

```yaml
id: Q-001
question: それはいつ同じものではなくなるか？
purpose: 同一性とライフサイクル境界の抽出
use_when: Entity候補の定義が曖昧
expected_signal: 終了条件、再生成、版、履歴
information_gain: high
```

## Evidence maturity

- `Observation`: 単一事例で発見
- `Provisional`: 複数回または複数例で有効
- `Validated`: 異なるドメインで再現
- `Core`: 安定し、高頻度で高効果
- `Deprecated`: より良いパターンへ統合または反証

## Retrieval

新しい対象の特徴を抽出する。

- 階層 / ネットワーク
- 状態変化の強さ
- 時間依存性
- 所有者数
- 境界数
- ルール密度
- 例外密度
- 推論の必要性
- 監査・履歴要求

パターン候補は名称類似ではなく、問題構造・適用条件・過去の結果で順位付けする。
