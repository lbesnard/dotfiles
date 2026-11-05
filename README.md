# dotfiles

Configuration for the machines I use: laptop (i3), remote servers, a home server and
a phone (Termux). One repo, linked into `$HOME` with [dotbot](https://github.com/anishathalye/dotbot).

![Workspace example](laptop.png "i3 + i3blocks + tmux + neovim + yazi...")

## What's in it

* **Shell**: [zsh](https://www.zsh.org/) with [zinit](https://github.com/zdharma-continuum/zinit) turbo mode
  (plugins load *after* the first prompt, so startup is ~50 ms),
  [starship](https://starship.rs) prompt, [zoxide](https://github.com/ajeetdsouza/zoxide) (`j`),
  [fzf](https://github.com/junegunn/fzf) + [fzf-tab](https://github.com/Aloxaf/fzf-tab)
* **Terminal**: [tmux](https://github.com/tmux/tmux) (plugins via [tpm](https://github.com/tmux-plugins/tpm)),
  [ghostty](https://ghostty.org) / alacritty
* **Editor**: [neovim](https://neovim.io) with [LazyVim](https://www.lazyvim.org)
* **Files / search**: [yazi](https://yazi-rs.github.io), ranger, `fd`, `ripgrep`, `bat`, `eza`
* **Git**: [forgit](https://github.com/wfxr/forgit), [tig](https://github.com/jonas/tig),
  [gh](https://cli.github.com) with custom aliases (`bin/git-alias`, `bin/gh-aliases`)
* **Desktop**: i3, i3blocks, rofi
* **Misc**: [cheat](https://github.com/cheat/cheat), [lnav](https://lnav.org), taskwarrior, beets, cmus
* **Packages**: [zerobrew](https://zerobrew.rs) (fast, sudo-free Homebrew-compatible client), listed in [`Brewfile`](Brewfile)

## Install

Needs git and curl. If a private repo or submodule is involved, set up your SSH key first:

```bash
eval "$(ssh-agent -s)" && ssh-add     # ~/.ssh/id_rsa
```

### Any Linux/macOS machine, no sudo

```bash
curl -fsSL https://raw.githubusercontent.com/lbesnard/dotfiles/main/initsys.sh | bash
```

This installs zerobrew, makes a **shallow** clone of this repo into `~/github_repo/dotfiles`,
installs the `Brewfile` packages and links everything into `$HOME`. It is safe to re-run (it
updates instead of cloning again).

Add `-s -- --ansible` to also run the user-level roles of
[Fleet-Control](https://github.com/lbesnard/Fleet-Control/tree/master/ansible)
(miniforge, neovim, cheat):

```bash
curl -fsSL https://raw.githubusercontent.com/lbesnard/dotfiles/main/initsys.sh | bash -s -- --ansible
```

### Laptop (full system, sudo)

System packages, i3, fonts etc. are provisioned by Fleet-Control, which also installs these dotfiles:

```bash
ansible-pull -U https://github.com/lbesnard/Fleet-Control.git \
             -d ~/ansible_pull_tmp -i ansible/hosts ansible/local.yml -K
```

### Manual

```bash
git clone --depth 1 https://github.com/lbesnard/dotfiles.git ~/github_repo/dotfiles
cd ~/github_repo/dotfiles
./install          # fetches submodules (shallow) and links the files listed in install.conf.yaml
```

Re-run `./install` after adding a link to `install.conf.yaml`.

### Termux (Android)

```bash
pkg install git curl zsh starship zoxide fzf fd bat eza ripgrep openssh tmux
git clone --depth 1 https://github.com/lbesnard/dotfiles.git ~/dotfiles
cd ~/dotfiles && ./install && chsh -s zsh
```

Use `pkg` rather than zerobrew here: zerobrew's binaries are built for glibc, Termux uses bionic.
`zsh/zshrc.termux` is a self-contained, minimal config. Set `TERMUX_TMUX=1` in `~/.alias.termux` to
autostart tmux.

## How the zsh config is organised

| File | Role |
| --- | --- |
| `zsh/zshrc` | Detects the machine profile once (`termux`, `server`, `homeserver`, `laptop`; override with `ZSH_PROFILE_NAME`) and sources the right files |
| `zsh/zshrc.common` | Shared config: tmux autostart (first, so the outer shell does no wasted work), zerobrew PATH, prompt, turbo-loaded plugins, fzf, completion styling |
| `zsh/zshrc.laptop`, `.server`, `.homeserver` | Per-machine additions |
| `zsh/zshrc.termux` | Standalone Termux config |
| `zsh/functions/`, `zsh/completions/` | Autoloaded functions and completions |
| `alias`, `alias_forgit` | Aliases and helper functions (loaded last so they override plugin aliases) |
| `config/starship.toml` | Prompt config |

Profile startup with `ZSH_PROFILE=1 zsh -i -c exit` (prints a zprof report), or
`for i in {1..5}; do time zsh -i -c exit; done`.

## Adding a package

```bash
zb install <formula>
zb bundle dump -f Brewfile --force     # keep Brewfile in sync
```

## Layout

```
install, install.conf.yaml   dotbot entrypoint and link map
initsys.sh, Brewfile         bootstrap for fresh machines
zsh/ tmux/ nvim/ config/     tool configs (config/* is linked into ~/.config)
bin/                         scripts, put on $PATH as ~/bin
```
