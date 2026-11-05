#!/data/data/com.termux/files/usr/bin/sh
#
# Bootstrap these dotfiles on Termux (Android). Plain `pkg`, no zerobrew:
# zerobrew binaries are glibc builds, Termux is bionic.
#
# Usage (inside Termux):
#   curl -fsSL https://raw.githubusercontent.com/lbesnard/dotfiles/main/termux-install.sh | sh
#
# If even `curl`/`git` fail with "cannot locate symbol ... libcurl/libssl", the packages
# are out of sync; run this first, then retry:
#   pkg update -y && pkg upgrade -y
#
# Env: DOTFILES_DIR (default: ~/dotfiles), DOTFILES_REPO

set -eu

DOTFILES_REPO="${DOTFILES_REPO:-https://github.com/lbesnard/dotfiles.git}"
DOTFILES_DIR="${DOTFILES_DIR:-$HOME/dotfiles}"

log() { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
die() { printf 'error: %s\n' "$*" >&2; exit 1; }

[ -n "${PREFIX:-}" ] && case "$PREFIX" in *com.termux*) ;; *) die "this script is for Termux only" ;; esac
command -v pkg >/dev/null || die "pkg not found: this script is for Termux only"

# --- 1. packages -------------------------------------------------------------
# A full upgrade first: a partial one (new git, old openssl) is what breaks
# git-remote-https with 'cannot locate symbol SSL_set_quic_tls_early_data_enabled'.
log "Updating Termux packages"
pkg update -y
pkg upgrade -y -o Dpkg::Options::=--force-confnew

# Core tools: must install, the setup is useless without them.
log "Installing core packages"
pkg install -y git curl zsh tmux perl starship zoxide fzf openssh neovim

# Extras (Termux equivalents of Fleet-Control's homebrew_packages.yml). Installed one by one
# so a package missing from the Termux repo is skipped instead of aborting the script.
# Not in Termux: act, angle-grinder, awscli (pip), mdcat, termshark, xclip (use termux-api), ueberzugpp.
EXTRAS="
    clang cmake ruby nodejs python
    autojump bat btop coreutils croc dust eza fd git-delta gh git-extras glow
    hexyl htop httpie hugo lazygit lazydocker lf lnav lsd mc ncdu p7zip poppler
    ranger rclone ripgrep sad taskwarrior the-silver-searcher tig tldr tree
    vim viu yazi yq
"
log "Installing extra packages"
skipped=""
for p in $EXTRAS; do
    pkg install -y "$p" >/dev/null 2>&1 && echo "  + $p" || skipped="$skipped $p"
done
[ -z "$skipped" ] || echo "  not installed (unavailable or failed):$skipped"

# --- 2. dotfiles -------------------------------------------------------------
if [ -d "$DOTFILES_DIR/.git" ]; then
    log "Updating dotfiles in $DOTFILES_DIR"
    git -C "$DOTFILES_DIR" pull --ff-only
else
    log "Cloning dotfiles into $DOTFILES_DIR"
    git clone --depth 1 "$DOTFILES_REPO" "$DOTFILES_DIR"
fi

# --- 3. link only what Termux uses -------------------------------------------
# (not ./install: it pulls every submodule - beets, cheat community... - and links
# desktop configs that make no sense on a phone)
link() {  # link <repo-relative source> <target>
    mkdir -p "$(dirname "$2")"
    ln -sfn "$DOTFILES_DIR/$1" "$2"
    echo "  $2 -> $1"
}
log "Linking dotfiles"
link zsh/zshrc               "$HOME/.zshrc"
link zsh/zshrc.termux        "$HOME/.zshrc.termux"
link tmux/tmux.conf          "$HOME/.tmux.conf"
link tmux/tmux.conf.termux   "$HOME/.tmux.conf.local"
link config/starship.toml    "$HOME/.config/starship.toml"
link bin                     "$HOME/bin"

# --- 4. default shell --------------------------------------------------------
if [ "$(basename "${SHELL:-}")" != zsh ]; then
    log "Setting zsh as the login shell"
    chsh -s zsh
fi

log "Done. Restart Termux (or run: exec zsh)."
echo "Optional: pkg install termux-services termux-api   # ssh-agent/sshd services, Android clipboard"
echo "tmux starts automatically; to disable: echo 'export TERMUX_NO_TMUX=1' >> ~/.zshenv"
