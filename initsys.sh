#!/usr/bin/env bash
#
# Bootstrap a working shell environment in $HOME (no sudo needed):
#   1. zerobrew (fast Homebrew-compatible package manager)  https://zerobrew.rs
#   2. the CLI tools listed in ./Brewfile
#   3. a shallow clone of these dotfiles, linked into $HOME with dotbot
#   4. (optional) the user-level ansible roles from Fleet-Control
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/lbesnard/dotfiles/main/initsys.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/lbesnard/dotfiles/main/initsys.sh | bash -s -- --ansible
#
# Options:
#   --ansible   also run Fleet-Control's remote.yml (miniforge, neovim, cheat) via ansible-pull
#   -h, --help  show this help
#
# Env: DOTFILES_DIR (default: ~/github_repo/dotfiles), DOTFILES_REPO (default: https over https)

set -euo pipefail

DOTFILES_REPO="${DOTFILES_REPO:-https://github.com/lbesnard/dotfiles.git}"
DOTFILES_DIR="${DOTFILES_DIR:-$HOME/github_repo/dotfiles}"
FLEET_REPO="https://github.com/lbesnard/Fleet-Control.git"
ZEROBREW_BIN="${ZEROBREW_BIN:-$HOME/.local/bin}"

run_ansible=0
for arg in "$@"; do
    case "$arg" in
        --ansible) run_ansible=1 ;;
        -h|--help) sed -n '2,17p' "$0" 2>/dev/null || true; exit 0 ;;
        *) echo "unknown option: $arg" >&2; exit 2 ;;
    esac
done

log() { printf '\033[1;34m==>\033[0m %s\n' "$*"; }

for cmd in curl git; do
    command -v "$cmd" >/dev/null || { echo "missing required command: $cmd" >&2; exit 1; }
done

# --- 1. zerobrew -------------------------------------------------------------
# --no-modify-path: PATH / cert env is already handled by zsh/zshrc.common in these dotfiles.
export PATH="$ZEROBREW_BIN:$PATH"
if ! command -v zb >/dev/null; then
    log "Installing zerobrew"
    curl -fsSL https://zerobrew.rs/install | bash -s -- --no-modify-path
fi
zb --version

# --- 2. dotfiles (shallow: no need for the full history) ---------------------
if [[ -d "$DOTFILES_DIR/.git" ]]; then
    log "Updating dotfiles in $DOTFILES_DIR"
    git -C "$DOTFILES_DIR" pull --ff-only
else
    log "Cloning dotfiles into $DOTFILES_DIR"
    mkdir -p "$(dirname "$DOTFILES_DIR")"
    git clone --depth 1 "$DOTFILES_REPO" "$DOTFILES_DIR"
fi

# --- 3. packages -------------------------------------------------------------
log "Installing packages from Brewfile"
zb bundle install -f "$DOTFILES_DIR/Brewfile"

# --- 4. link dotfiles (./install also fetches the submodules, shallowly) -----
log "Linking dotfiles"
"$DOTFILES_DIR/install"

# --- 5. optional: ansible roles (miniforge, neovim, cheat) -------------------
# The brew/dotfiles tags are intentionally skipped: zerobrew + dotbot above replace them.
if (( run_ansible )); then
    log "Running Fleet-Control ansible (miniforge, neovim, cheat)"
    command -v ansible-pull >/dev/null || zb install ansible
    ansible-pull -U "$FLEET_REPO" -d "$HOME/.cache/ansible_pull" \
        -i ansible/hosts ansible/remote.yml -t miniforge,neovim,cheat
fi

log "Done. Start a new shell: exec zsh"
