.PHONY: macos
macos: macos_init link homebrew brew_bundle font

.PHONY: macos_init
macos_init:
	bin/macos_init.sh

.PHONY: homebrew
homebrew:
	bin/homebrew.sh

.PHONY: brew_bundle
brew_bundle_biz:
	brew bundle

.PHONY: source
source:
	source ~/.zshenv

.PHONY: link
link:
	bin/link.sh

.PHONY: font
font:
	bin/font.sh

.PHONY: sdkman
sdkman:
	bin/sdkman.sh
