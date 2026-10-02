# Challenge and Quality

## Review lenses

### Semantic
- 定義が循環していないか
- 同義語・多義語が放置されていないか
- 上位概念と下位概念の基準が一貫するか

### Identity and lifecycle
- 同一性の基準は何か
- 生成・変更・終了主体は誰か
- 状態と履歴を混同していないか

### Boundary and ownership
- 一つの概念が複数境界で異なる意味を持たないか
- 制約を守る責任者が明確か
- 境界間の翻訳が必要か

### Rules and exceptions
- ルールの前提条件は明示されているか
- 例外が場当たり的な属性追加になっていないか
- 禁止・必須・導出を区別しているか

### Time
- 現在値、予定、履歴、発生日、記録日を区別しているか
- 遡及変更や同時発生を扱えるか

### Purpose fit
- このモデルで目的の質問に答えられるか
- 詳細が意思決定に寄与しているか
- 別視点の要素が混入していないか

## Adversarial tests

- **Counterexample test**: 最小反例を作る
- **Boundary-case test**: 0件、1件、多数、同時、欠損、重複
- **Role reversal**: 主体と対象を逆にして不自然さを見る
- **Temporal test**: 過去・未来・取消・訂正・再開
- **Scale test**: 数、組織、地域、権限が100倍
- **Alternative decomposition**: 1概念を分割、複数概念を統合
- **Vocabulary substitution**: 用語を定義文に置換して意味が通るか
- **Decision simulation**: 実際の判断をモデルだけで再現できるか

## Issue severity

- `Critical`: 誤った意思決定・重大な矛盾・モデル目的を達成不能
- `Major`: 重要例外、境界、責任、時間軸の欠落
- `Minor`: 命名、説明不足、局所的な冗長性
- `Question`: 証拠不足で判断不能

## Quality dimensions

各1〜5。総合点ではなく弱点検出に使う。

- Purpose fitness
- Semantic clarity
- Completeness for decision
- Internal consistency
- Boundary integrity
- Traceability to evidence
- Uncertainty visibility
- Change localization
- Explainability
- Parsimony

## Exit policy

次をすべて満たしたら現在目的に対して終了可能。

1. Critical issue = 0
2. Major issueが受容または明示的に延期されている
3. 主要概念・関係・制約が証拠へ追跡可能
4. 代表例と重要例外を説明可能
5. 残るUnknownが対象意思決定を阻害しない
6. 次の反復コストが期待情報利得を上回る
