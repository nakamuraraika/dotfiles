# dotfiles

## Install

### for macOS

```sh
xcode-select --install
git clone https://github.com/nakamuraraika/dotfiles.git
cd dotfiles
make macos
```

## Personal agent skills

個人用Skillは、クライアントに依存しない [`skills/`](skills/) で管理します。
Codex / Claude Code へ配布する場合は、まず変更予定を確認してください。

```sh
python3 bin/link-skills.py
python3 bin/link-skills.py --apply
```

既存ファイルは上書きしません。同期方法・APM依存・旧リポジトリの扱いは
[Skillsの運用ガイド](skills/README.md) を参照してください。
