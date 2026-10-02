# 個人用 Skills

個人用Skillの正本は、このリポジトリの `skills/` です。Codex / Claude Code の
ディレクトリは配布先として扱い、編集はこのリポジトリで行います。

```text
skills/
├── core/          # 共通の開発手順
├── frontend/      # フロントエンド
├── backend/       # バックエンド
├── experimental/  # 試行中
└── meta/          # モデリング・評価
```

| Skill | 用途 |
| --- | --- |
| [rapid-ontology-modeling](meta/rapid-ontology-modeling/) | ドメインの構造化・モデリング |
| [evaluation-orchestrator](meta/evaluation-orchestrator/) | 評価手順の設計と実行 |
| [context-specific-evaluation](meta/context-specific-evaluation/) | 目的・文脈に応じた対象評価 |

## 配布と同期

Python 3 を使用します。保持する通常のcheckoutで、リポジトリ直下から実行します。
既存の `make macos` や `make link` からは自動実行しません。

```sh
python3 bin/link-skills.py          # 変更予定を確認。書き込みなし
python3 bin/link-skills.py --apply  # Codex / Claude Code へリンク
```

カテゴリを除いたSkill名で `~/.codex/skills/<name>` と
`~/.claude/skills/<name>` へリンクします。`CODEX_HOME` がある場合は
`$CODEX_HOME/skills` を使用します。片方だけなら `--target codex` または
`--target claude`、独自の配置先なら `--codex-dir PATH` / `--claude-dir PATH` を指定します。
同名Skillが複数カテゴリにある場合は停止します。

既存の同じリンクは維持します。それ以外のディレクトリ・ファイル・リンクが
同名で存在する場合は、全対象の事前確認で停止し、上書きも削除もしません。
競合するコピーにローカル変更がないか比較してから、別名へ退避して再実行してください。
例（`CONFLICT` に表示された実際のパスを使用）:

```sh
diff -ru "$HOME/.claude/skills/rapid-ontology-modeling" skills/meta/rapid-ontology-modeling
# 差分を確認した後、既存のコピーを退避する。-n は既存バックアップを上書きしない。
mv -n "$HOME/.claude/skills/rapid-ontology-modeling" "$HOME/.claude/skills/rapid-ontology-modeling.before-dotfiles"
python3 bin/link-skills.py --apply
```

既存の実体をリンク先に持つシンボリックリンクの場合も、元の実体は削除しません。
実行中に権限エラー等で失敗した場合は、原因を解消して再実行できます。
Skillを削除・改名した際の古いリンクは自動削除しないため、対象を確認して手動で外します。

編集・同期は次の流れです。

1. `skills/<category>/<name>/` を編集し、Skill固有の検証を実行する。
2. 差分を確認してコミット・PRを作成する。
3. 他の端末では `git pull --ff-only`、新規Skill追加時は上記の配布コマンドも再実行する。

既存Skillの内容はリンク経由で反映されます。必要なら利用するエージェントの
セッションを再開して読み直します。checkoutを移動した場合は、古いリンクを
確認して外した後、配布コマンドを再実行します。配布先を別ツールと同時管理しません。
ロールバックは、今回作成したリンクだけを外し、退避したコピーを元の名前へ戻します。

## 外部Skill

個人用SkillはGitとリンクで管理・配布できるため、APMは使用しません。
元リポジトリの `apm.yml`、`apm.lock.yaml`、配布済みの `.claude/skills/` は移行対象外です。

旧環境が参照していた外部Skillは、取得元の記録だけを残します。

- 取得元: `mizchi/skills/meta/empirical-prompt-tuning`
- コミット: `5aaf2d126a04a8b079fd5184eb1860f232afffd3`

この外部Skillは今回の管理・配布対象に含めません。必要になった時点で、
導入方法と更新方法を決めます。独自の依存管理用manifestやlockも追加しません。

## 移行元と保留事項

移行元: [nakamuraraika/skills](https://github.com/nakamuraraika/skills)、
コミット `2fa6aa8bd057057232059641d4c58840963ca6fa`。
`meta/` 以下の3つのSkillは補助ファイル・実行権限を含めてそのままコピーしました。
機械可読の移行記録は [migration.json](migration.json) にあります。
元READMEのライセンス表記は「MIT unless a skill directory carries its own LICENSE.txt」です。

PRのマージ後、個人用Skillの更新先をこちらへ切り替えます。
旧リポジトリは削除せず、**deprecated / archive候補**として保持します。
既存利用者・外部ツールからの参照先、全端末の切り替えを確認してから、旧READMEへ
移行先を案内し、アーカイブを別作業として判断します。今回は旧リポジトリを変更しません。

2026-10-02の確認では、ローカルの旧リポジトリに `design/ontology-modeling`、
`design/decision-evaluation` への改名、`context-specific-evaluation` の削除、
`meta/skill-building` の追加を含む未コミットの再編がありました。
今回の移行には混ぜず、元の作業ディレクトリを保持しています。
**旧リポジトリをアーカイブする前に、この再編を別PRで取り込むか判断してください。**
