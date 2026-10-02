# Framing and Extraction

## Frame canvas

| Field | Question |
|---|---|
| Purpose | このモデルによって何が可能になるか |
| Consumer | 誰が読む・使うか |
| Decision | どの判断を支援するか |
| Scope | 何を含み、何を含めないか |
| Perspective | business / domain / data / process / security / organization / time |
| Abstraction | ecosystem / capability / domain / concept / attribute / implementation |
| Time horizon | 現在、将来、履歴のどれを扱うか |
| Evidence | ヒアリング、文書、実例、ログ、既存システム |
| Precision | 探索用、合意形成用、実装入力用、機械推論用 |

## Extraction units

- **Concept**: 独立して識別・定義する価値があるもの
- **Role**: 文脈によって主体が担う振る舞い
- **Relation**: 二つ以上の概念間の意味ある接続
- **Property**: 概念を記述する特徴
- **Rule**: 条件から結果・可否を決めるもの
- **Constraint**: 常に満たす必要がある条件
- **Event**: 意味のある状態変化を表す過去形の事実
- **State**: 可能な振る舞い・遷移を変える持続的条件
- **Lifecycle**: 生成から終了までの時間的構造
- **Boundary**: 用語、責任、整合性、所有の切れ目
- **Exception**: 通常規則が成立しないケース
- **Evidence**: 主張を支える観測可能な根拠

## Evidence labels

- `F` Fact: 原文・観測・合意で直接確認済み
- `I` Interpretation: 事実から妥当に読める解釈
- `H` Hypothesis: 検証が必要なモデル仮説
- `U` Unknown: 情報がない
- `C` Conflict: 情報源間で対立

各重要要素にラベルと出典を付ける。

## Concept card

```yaml
id: C-001
name: Favorite
aliases: [お気に入り]
definition: ユーザーが作品への継続的関心を明示した状態または記録
identity_criterion: user_id + work_id
examples: []
counterexamples: []
properties: []
relations: []
lifecycle: []
evidence_status: H
source: interview-01
open_questions: []
```

## High-information-gain questions

質問候補を以下で評価する。

`IG = structural_impact × uncertainty × decision_risk ÷ answer_cost`

厳密な数値計算は不要。相対順位に使う。

高レバレッジな質問:

- AとBを同じものとして扱えない具体例はあるか
- これは誰の責任で生成・変更・終了するか
- いつからいつまで同一のものとみなすか
- この規則が成立しない最小の例外は何か
- この情報が変わると、どの判断・処理が変わるか
- 失われると復元できない事実は何か
- 現在状態と履歴のどちらが業務上重要か
- この語を別部門はどう呼び、意味は同じか

## Extraction discipline

- 名詞をすべて概念にしない。識別、責任、規則への寄与を確認する。
- 動詞は関係、コマンド、イベント、能力の候補として分析する。
- 形容詞は状態、分類、評価軸、派生値の候補として分析する。
- UI項目やDB列を、そのままドメイン概念とみなさない。
- 具体例を最低1つ、反例を最低1つ用いて定義を検証する。
