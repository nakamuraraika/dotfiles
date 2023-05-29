#!/bin/bash -eu

mkdir -p .temp
curl -s https://api.github.com/repos/yuru7/HackGen/releases/latest | jq -r '.assets | map(select(.name | startswith("HackGen_NF_"))) | sort_by(.created_at) | last | .browser_download_url' | xargs curl -Lo .temp/HackGen_NF.zip
unzip -qod .temp .temp/HackGen_NF.zip

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  mkdir -p ~/.fonts
  FONT_DIR=~/.fonts
elif [[ "$OSTYPE" == "darwin"* ]]; then
  FONT_DIR=~/Library/Fonts
fi

cp -rf .temp/HackGen_NF_*/* "$FONT_DIR"

rm -rf .temp
