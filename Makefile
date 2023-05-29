.PHONY: macos
macos: link homebrew brew_bundle font

.PHONY: macos_init
macos_init:
	source bin/macos_init.sh

.PHONY: homebrew
homebrew:
	source bin/homebrew.sh

.PHONY: brew_bundle
brew_bundle_biz:
	brew bundle

.PHONY: source
source:
	source ~/.zshenv

.PHONY: link
link:
	source bin/link.sh

.PHONY: font
font:
	source bin/font.sh

.PHONY: sdkman
sdkman:
	source bin/sdkman.sh
