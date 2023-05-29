export XDG_CONFIG_HOME="${HOME}/.config"
export ZDOTDIR="$XDG_CONFIG_HOME/zsh"
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export PATH=$HOME/bin:PATH

test -d ~/.linuxbrew && eval "$(~/.linuxbrew/bin/brew shellenv)"
test -d /home/linuxbrew/.linuxbrew && eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
test -d /opt/homebrew/ && eval "$(/opt/homebrew/bin/brew shellenv)"
