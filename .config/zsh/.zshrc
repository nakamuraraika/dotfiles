test -d ~/.linuxbrew && eval "$(~/.linuxbrew/bin/brew shellenv)"
test -d /home/linuxbrew/.linuxbrew && eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
test -d /opt/homebrew/ && eval "$(/opt/homebrew/bin/brew shellenv)"

export CARGO_HOME=$HOME/.cargo
export PATH=$CARGO_HOME/bin:$PATH

plugins=(git ssh-agent)

eval "$(starship init zsh)"

export SDKMAN_DIR=$(brew --prefix sdkman-cli)/libexec
[[ -s "${SDKMAN_DIR}/bin/sdkman-init.sh" ]] && source "${SDKMAN_DIR}/bin/sdkman-init.sh"
# fnm settings
eval "$(fnm env --use-on-cd)"

### MANAGED BY RANCHER DESKTOP START (DO NOT EDIT)
export PATH="/Users/nakamuraraika/.rd/bin:$PATH"
### MANAGED BY RANCHER DESKTOP END (DO NOT EDIT)
eval "$(frum init)"
