---
name: rapid-ontology-modeling
description: Use this skill when the user wants to understand, structure, model, or re-model a real-world domain, business process, product concept, data domain, ontology, taxonomy, knowledge graph, DDD domain model, conceptual model, or terminology system. Also use it when they ask to extract concepts and relationships, clarify boundaries, resolve ambiguous vocabulary, review an existing model, preserve modeling decisions, run fast modeling feedback loops, mine reusable patterns, or turn interviews and source material into an evolving model. Trigger on phrases such as オントロジー化, モデリング, 概念モデル, ドメインモデル, 概念抽出, 関係整理, 境界整理, 用語整理, モデルレビュー, knowledge graph, ontology, taxonomy, conceptual model, domain modeling, ubiquitous language, and model refinement.
version: 1.0.0
---

# Rapid Ontology Modeling

現実世界に対する理解を、意思決定可能な構造へ高速に圧縮し、反証によって更新し続ける。

モデル完成を目的にしない。**重要な不確実性を減らし、次の意思決定を可能にすること**を目的とする。

## Core loop

常に次の最小ループを回す。

1. **Frame** — 目的、利用者、意思決定、対象範囲、視点、抽象度を固定する
2. **Extract** — 概念、関係、ルール、制約、状態、イベント、例外、不確実性を抽出する
3. **Model** — 最小の仮説モデル `n` を作る
4. **Expose** — 変更点、重要発見、判断根拠、未解決点だけをハイライトする
5. **Challenge** — 反例・境界事例・代替モデルで壊す
6. **Learn** — 理解の変化を記録し、モデル `n+1` と次の質問を作る
7. **Mine** — 再利用可能なパターン、質問、アンチパターンを抽出する

完全な情報収集後にモデルを作らない。**小さなモデルを早く外在化し、最も情報利得の高いフィードバックを得る。**

## Operating rules

- 最初のモデルは粗くてよいが、暗黙の推測を混ぜない。
- 事実、解釈、仮説、未確認を必ず分離する。
- ヒアリングを網羅質問から始めず、現在のモデルを最も変えうる質問から聞く。
- 同一ビューに異なる抽象度や関心事を混ぜない。
- 「正しい唯一のモデル」を探さず、目的に対するモデル適合度を評価する。
- 結論だけでなく、判断理由、棄却案、理解の変化を保存する。
- 各反復では全文ではなく差分と影響範囲をレビューする。
- 不明点を無理に埋めない。未確認事項はモデル上の一級要素として扱う。
- モデル表記法は目的に合わせて選ぶ。表記法を先に固定しない。
- 重大な不確実性が残る限り、見た目の整形より学習を優先する。

## Start protocol

依頼を受けたら、まず次を特定する。明示されていない項目は暫定仮説として表示する。

- モデルの目的
- モデルを使う主体
- 支援する意思決定または説明
- 対象範囲と範囲外
- 主視点
- 期待する抽象度
- 利用可能な証拠
- 時間制約と必要精度

`references/framing-and-extraction.md` を必要に応じて読む。

## Iteration protocol

### 1. Create the working frame

`templates/model-workspace.md` を基にワークスペースを作る。

スコープが曖昧でも停止しない。暫定フレームを置き、モデルを変えそうな前提を `Assumption` として露出する。

### 2. Build model n1 immediately

入力から最小限の概念・関係・制約を抽出し、最初のモデルを提示する。

モデルには最低限、以下を含める。

- Concept: 何であるか
- Relation: どう関係するか
- Constraint: 何が成立条件か
- Lifecycle / State: いつ変化するか
- Boundary: どこまで同じ責任・意味体系か
- Evidence status: Confirmed / Interpreted / Hypothesis / Unknown

### 3. Generate the delta highlight

各反復後、必ず次だけを先頭に出す。

- 新しく分かったこと
- モデルを変えたこと
- 重要な判断と理由
- 最大の未解決点
- 次に確認すべき一点

### 4. Select feedback by information gain

質問は一度に大量提示しない。候補質問を次の観点で順位付けし、上位1〜3件だけを扱う。

- 回答によって境界が変わる可能性
- 複数概念の意味を同時に確定できるか
- 誤った実装・意思決定を防げるか
- 回答コストが低いか
- 現在の最大リスクを減らすか

### 5. Challenge the model

通常レビューだけでなく、独立した反証を行う。必要に応じて `references/challenge-and-quality.md` を読む。

最低限確認する。

- 代表例だけでなく例外でも成立するか
- 同じ語が複数の意味を持っていないか
- 異なる語が同じ概念を表していないか
- 所有者、責任、ライフサイクルが一貫するか
- 時間・履歴・状態遷移が欠落していないか
- 境界を越える制約が暗黙化していないか
- より単純な代替モデルで説明できないか
- 目的や視点が変わればモデルがどう変わるか

### 6. Update understanding, not only the diagram

モデル更新時は `Decision Log` と `Learning Log` を同時更新する。

- 何が変わったか
- なぜ変わったか
- どの証拠で変わったか
- どの旧仮説を棄却したか
- 影響範囲はどこか
- 次に何を検証するか

### 7. Mine reusable knowledge

意味のある反復が完了したら `references/pattern-system.md` を読む。

以下を候補として抽出する。

- Pattern: 再利用可能な問題構造と解法
- Anti-pattern: 失敗構造、検知兆候、防止策
- Question: 高い情報利得を生んだ質問
- Heuristic: 条件付きの経験則
- Evaluation rule: 再利用可能な評価基準

1事例だけで強い一般則に昇格させない。証拠レベルを付ける。

## Model views

単一の巨大モデルを作らず、必要なビューに分ける。

- **Vocabulary view** — 用語、定義、同義語、禁用語
- **Concept view** — 概念、分類、包含、同一性
- **Relationship view** — 関係、方向、多重度、依存
- **Lifecycle view** — 生成、状態、イベント、終了
- **Rule view** — 成立条件、禁止、例外、導出規則
- **Boundary view** — 文脈、所有、整合性、翻訳
- **Evidence view** — 根拠、不確実性、対立情報
- **Decision view** — 採用案、棄却案、トレードオフ

## Representation selection

- 用語体系・分類: glossary / taxonomy / concept map
- 意味関係・推論: ontology / RDF-style triples / knowledge graph
- 業務責任・境界: DDD context map / domain model
- データ構造: conceptual ER model
- 状態変化: state machine
- 時系列の相互作用: event model / sequence / workflow
- 原因と結果: causal graph

複数表現を使う場合は、同じ概念IDを共有し、表記間の意味ずれを防ぐ。

## Quality gates

固定の総合点だけで終了判定しない。目的別に重要度を変える。

必須ゲート:

- 重大な矛盾がない
- 重要概念に定義と識別基準がある
- 主要関係に意味と方向がある
- 重要制約と例外が露出している
- 事実と仮説が分離されている
- 主要判断に根拠がある
- モデルが対象の意思決定を実際に支援できる

収束の兆候:

- 新情報による構造変更が局所化している
- 同じ質問への回答が一貫する
- 新しい事例を既存概念で説明できる
- 重大Issueがない
- 残るUnknownが意思決定を妨げない

詳細は `references/challenge-and-quality.md` を読む。

## Output contract

通常の最終出力は次の順序にする。

1. **Current understanding** — 現在の理解を短く説明
2. **Highlights since previous iteration** — 差分と学習
3. **Current model** — 適切な表現で提示
4. **Evidence and uncertainty** — 事実・解釈・仮説・未確認
5. **Key decisions** — 判断、理由、棄却案
6. **Critical issues** — モデルを壊しうる論点
7. **Next feedback target** — 次に答える価値が最も高い質問
8. **Reusable knowledge mined** — パターン等。存在する場合のみ

## Orchestration

サブエージェントを利用できる場合、初期モデル作成後に独立して次を実行する。

1. **Evidence Extractor** — 原文から主張と証拠を抽出し、推測を排除
2. **Concept Modeler** — 概念・関係・境界の最小モデルを作成
3. **Adversarial Reviewer** — 反例、矛盾、例外、隠れた前提を抽出
4. **Alternative Modeler** — 異なる切り口の代替モデルを作成
5. **Synthesizer** — 重複排除し、差分、決定、未解決を統合
6. **Pattern Miner** — 再利用知識を抽出

各エージェントには全文履歴を渡さず、役割に必要な入力と成果物パスだけを渡す。統合前に独立性を保つ。

詳細は `references/orchestration.md` を読む。

## Failure handling

- 情報不足: 推測で完成させず、暫定モデルと高情報利得質問を出す
- 意見対立: 勝手に統合せず、視点・前提・用語の差として並置する
- 抽象化過多: 実例と反例へ戻り、識別基準を作る
- 詳細化過多: 支援する意思決定に寄与しない要素を別ビューへ退避する
- モデル肥大化: 境界・視点・時間軸で分割する
- ループ停滞: 表現の修正ではなく、新しい証拠または反証を投入する
- レビューが長い: 全文レビューをやめ、差分・影響範囲・最大リスクへ限定する

## References

必要なときだけ読む。

- `references/framing-and-extraction.md`
- `references/challenge-and-quality.md`
- `references/pattern-system.md`
- `references/orchestration.md`
- `references/artifact-schema.md`
- `examples/anime-favorite-example.md`
