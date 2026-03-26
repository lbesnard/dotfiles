# Keyboard Shortcuts Cheatsheet

> Search quickly with: `sk` (fzf shortcut finder)

---

## i3 Window Manager

| Shortcut | Tool | Description |
|----------|------|-------------|
| `$mod+Return` | i3 | Open terminal |
| `$mod+q` | i3 | Open file manager (PCManFM) |
| `$mod+i` | i3 | Open Firefox |
| `$mod+d` | i3 | Launch application menu |
| `$mod+Shift+q` | i3 | Kill focused window |
| `$mod+h` | i3 | Focus left |
| `$mod+j` | i3 | Focus down |
| `$mod+k` | i3 | Focus up |
| `$mod+l` | i3 | Focus right |
| `$mod+Left` | i3 | Focus left (arrow) |
| `$mod+Down` | i3 | Focus down (arrow) |
| `$mod+Up` | i3 | Focus up (arrow) |
| `$mod+Right` | i3 | Focus right (arrow) |
| `$mod+space` | i3 | Toggle focus tiling/floating |
| `$mod+a` | i3 | Focus parent container |
| `$mod+Shift+h` | i3 | Move window left |
| `$mod+Shift+j` | i3 | Move window down |
| `$mod+Shift+k` | i3 | Move window up |
| `$mod+Shift+l` | i3 | Move window right |
| `$mod+z` | i3 | Split horizontally |
| `$mod+v` | i3 | Split vertically |
| `$mod+f` | i3 | Toggle fullscreen |
| `$mod+s` | i3 | Layout stacking |
| `$mod+w` | i3 | Layout tabbed |
| `$mod+e` | i3 | Layout toggle split |
| `$mod+Shift+space` | i3 | Toggle tiling/floating |
| `$mod+1` | i3 | Switch to workspace 1 |
| `$mod+2` | i3 | Switch to workspace 2 |
| `$mod+3` | i3 | Switch to workspace 3 |
| `$mod+4` | i3 | Switch to workspace 4 |
| `$mod+5` | i3 | Switch to workspace 5 |
| `$mod+6` | i3 | Switch to workspace 6 |
| `$mod+7` | i3 | Switch to workspace 7 |
| `$mod+8` | i3 | Switch to workspace 8 |
| `$mod+9` | i3 | Switch to workspace 9 |
| `$mod+0` | i3 | Switch to workspace 10 |
| `$mod+Shift+1` | i3 | Move window to workspace 1 |
| `$mod+Shift+2` | i3 | Move window to workspace 2 |
| `$mod+Shift+3` | i3 | Move window to workspace 3 |
| `$mod+Shift+4` | i3 | Move window to workspace 4 |
| `$mod+Shift+5` | i3 | Move window to workspace 5 |
| `$mod+Shift+6` | i3 | Move window to workspace 6 |
| `$mod+Shift+7` | i3 | Move window to workspace 7 |
| `$mod+Shift+8` | i3 | Move window to workspace 8 |
| `$mod+Shift+9` | i3 | Move window to workspace 9 |
| `$mod+Shift+0` | i3 | Move window to workspace 10 |
| `$mod+r` | i3 | Enter resize mode |
| `$mod+p` | i3 | Display settings / change display |
| `$mod+Shift+c` | i3 | Reload i3 configuration |
| `$mod+Shift+r` | i3 | Restart i3 in-place |
| `$mod+Shift+e` | i3 | Exit i3 |
| `Ctrl+Alt+L` | i3 | Lock screen |
| `Print` | i3 | Take screenshot |
| `XF86AudioRaiseVolume` | i3 | Increase volume +2% |
| `XF86AudioLowerVolume` | i3 | Decrease volume -2% |
| `XF86AudioMute` | i3 | Toggle audio mute |
| `XF86MonBrightnessUp` | i3 | Increase screen brightness +5% |
| `XF86MonBrightnessDown` | i3 | Decrease screen brightness -5% |
| `Ctrl+Shift+U` | i3 | KeePass: type username+password (passhole) |
| `Ctrl+Shift+K` | i3 | KeePass: type password only (passhole) |

### i3 Resize Mode (enter with `$mod+r`)

| Shortcut | Tool | Description |
|----------|------|-------------|
| `h` | i3 resize | Shrink window width |
| `j` | i3 resize | Grow window height |
| `k` | i3 resize | Shrink window height |
| `l` | i3 resize | Grow window width |
| `Return` | i3 resize | Exit resize mode |
| `Escape` | i3 resize | Exit resize mode |

---

## tmux (prefix: `Ctrl+A`)

| Shortcut | Tool | Description |
|----------|------|-------------|
| `Ctrl+A` | tmux | Prefix key |
| `prefix+e` | tmux | Edit tmux config in new window |
| `prefix+r` | tmux | Reload tmux configuration |
| `Ctrl+L` | tmux | Clear history and screen |
| `prefix+Ctrl+C` | tmux | Create new session |
| `prefix+Ctrl+F` | tmux | Find and switch session |
| `prefix+BTab` | tmux | Switch to last session |
| `prefix+Tab` | tmux | Switch to last active window |
| `prefix+Ctrl+H` | tmux | Select previous window |
| `prefix+Ctrl+L` | tmux | Select next window |
| `prefix+h` | tmux | Move to left pane |
| `prefix+j` | tmux | Move to down pane |
| `prefix+k` | tmux | Move to up pane |
| `prefix+l` | tmux | Move to right pane |
| `prefix+>` | tmux | Swap pane with next |
| `prefix+<` | tmux | Swap pane with previous |
| `prefix+Shift+H` | tmux | Resize pane left |
| `prefix+Shift+J` | tmux | Resize pane down |
| `prefix+Shift+K` | tmux | Resize pane up |
| `prefix+Shift+L` | tmux | Resize pane right |
| `prefix+-` | tmux | Split window vertically |
| `prefix+_` | tmux | Split window horizontally |
| `prefix++` | tmux | Maximize/zoom current pane |
| `prefix+m` | tmux | Toggle mouse mode |
| `prefix+U` | tmux | URL viewer |
| `prefix+F` | tmux | File picker (fpp) |
| `prefix+Enter` | tmux | Enter copy mode |
| `prefix+b` | tmux | List paste buffers |
| `prefix+p` | tmux | Paste from top buffer |
| `prefix+P` | tmux | Choose buffer to paste |

### tmux Copy Mode (vi-style)

| Shortcut | Tool | Description |
|----------|------|-------------|
| `v` | tmux copy | Begin selection |
| `Ctrl+V` | tmux copy | Toggle rectangle selection |
| `y` | tmux copy | Copy selection to clipboard |
| `Escape` | tmux copy | Cancel / exit copy mode |
| `H` | tmux copy | Jump to start of line |
| `L` | tmux copy | Jump to end of line |

---

## KeePass / Passhole

| Shortcut | Tool | Description |
|----------|------|-------------|
| `Ctrl+Shift+U` | keepass | Type username+password (tabbed) via passhole-fzf |
| `Ctrl+Shift+K` | keepass | Type password only via passhole-fzf |

---

## Zsh / Shell

| Shortcut | Tool | Description |
|----------|------|-------------|
| `Ctrl+E` | zsh | Open file in vim via fzf picker |
| `Ctrl+N` | zsh | View ncdump output via fzf netcdf picker |
| `Ctrl+T` | zsh | FZF file picker |
| `Ctrl+R` | zsh | FZF history search |
| `Alt+C` | zsh | FZF directory picker |
| `Home` | zsh | Jump to beginning of line |
| `End` | zsh | Jump to end of line |
| `Delete` | zsh | Delete character |
| `Alt+A` | fzf | Select all items |
| `Alt+D` | fzf | Deselect all items |
| `Alt+T` | fzf | Toggle all items |
| `Alt+Y` | fzf | Copy selected to clipboard |
| `Alt+E` | fzf | Open selected in nvim |
| `Alt+V` | fzf | Open selected in VSCode |
| `?` | fzf | Toggle preview pane |

---

## Vim

| Shortcut | Tool | Description |
|----------|------|-------------|
| `<Leader>f` | vim | Fuzzy find files |
| `<Leader><Space>` | vim | Clear search highlighting |
| `<Leader>S` | vim | Remove trailing whitespace |
| `<Leader>q` | vim | Quit without saving |
| `<Leader>yy` | vim | Yank line to system clipboard |
| `<Leader>YY` | vim | Yank entire file to system clipboard |
| `<Leader>p` | vim | Paste from system clipboard |
| `Ctrl+C` | vim | Copy selection to clipboard (visual) |
| `Ctrl+T` | vim | Toggle NERDTree |
| `Ctrl+P` | vim | CtrlP file search |
| `Ctrl+B` | vim | Open tag in new tab |
| `Alt+]` | vim | Open tag in vertical split |
| `Ctrl+W Left` | vim | Vertical resize +5 |
| `Ctrl+W Right` | vim | Vertical resize -5 |
| `Ctrl+W Up` | vim | Resize height +5 |
| `Ctrl+W Down` | vim | Resize height -5 |
| `Tab` | vim | Toggle fold (normal) / autocomplete next (insert) |
| `S-Tab` | vim | Autocomplete previous |
| `F5` | vim | Remove trailing whitespace |
| `F9` | vim | Execute current Python file |
| `<Leader>ff` | vim | Telescope: find files |
| `<Leader>fg` | vim | Telescope: live grep |
| `<Leader>fb` | vim | Telescope: buffers |
| `<Leader>fh` | vim | Telescope: help tags |
| `<Leader>b` | vim | Insert ipdb breakpoint (Python) |
| `<Leader>p` | vim | Insert pudb breakpoint (Python) |
| `<Leader>(` | vim | Jump to previous Python function |
| `<Leader>)` | vim | Jump to next Python function |
| `<Leader>nc` | vim | View ncdump in vertical split |
| `<Space>ga` | vim | Git add current file |
| `<Space>gs` | vim | Git status |
| `<Space>gc` | vim | Git commit |
| `<Space>gd` | vim | Git diff |
| `<Space>gl` | vim | Git log |
| `<Space>gp` | vim | Git grep |
| `<Space>gps` | vim | Git push |
| `<Space>gpl` | vim | Git pull |

### EasyMotion

| Shortcut | Tool | Description |
|----------|------|-------------|
| `s` | vim easymotion | Find 2 characters (jump anywhere) |
| `<Leader>L` | vim easymotion | Move to line |
| `<Leader>w` | vim easymotion | Move to word |

---

## LazyVim / Neovim

| Shortcut | Tool | Description |
|----------|------|-------------|
| `<Leader>cR` | lazyvim | Rename TypeScript file |
| `<Leader>co` | lazyvim | Organize imports |

> LazyVim default keymaps: https://www.lazyvim.org/keymaps

---

## Useful Aliases

| Shortcut | Tool | Description |
|----------|------|-------------|
| `..` | zsh alias | Go up one directory |
| `...` | zsh alias | Go up 3 directories |
| `g` | zsh alias | git |
| `ga` | forgit | Interactive git add |
| `gd` | forgit | Interactive git diff |
| `glo` | forgit | Interactive git log |
| `gcf` | forgit | Interactive git checkout file |
| `grh` | forgit | Interactive git reset HEAD |
| `gcp` | forgit | Interactive git cherry-pick |
| `gclean` | forgit | Interactive git clean |
| `t` | taskwarrior | Task command |
| `tt` | taskwarrior | Show today's tasks |
| `tui` | taskwarrior | Task terminal UI |
| `lock_screen` | zsh alias | Lock screen |
| `brightness_up` | zsh alias | Increase brightness |
| `brightness_down` | zsh alias | Decrease brightness |
| `docker_logs_tail` | zsh alias | Tail docker logs (fzf picker) |
| `docker_sh` | zsh alias | Shell into container (fzf picker) |
| `docker_rm` | zsh alias | Remove container (fzf picker) |
| `wg_bfunk_start` | zsh alias | Start WireGuard VPN |
| `wg_bfunk_stop` | zsh alias | Stop WireGuard VPN |
| `sk` | zsh alias | Search shortcuts with fzf |
| `cheat_fzf` | zsh alias | Search cheat sheets with fzf |
| `copy` | zsh alias | Copy to clipboard (xclip) |
| `yy` | zsh alias | Copy to clipboard (xclip) |
| `rsrc` | zsh alias | Reload shell config |
| `ports` | zsh alias | Show open ports (netstat) |
| `ssh-add` | zsh alias | Add SSH key for 10 hours |
| `vim_plugin_install` | zsh alias | Update vim plugins |
| `jupyter_lab_start` | zsh alias | Start Jupyter Lab |
| `screen_layout` | zsh alias | Interactive screen layout (arandr) |
| `display_docked_work` | zsh alias | Switch to docked work display |
| `display_docked_home` | zsh alias | Switch to docked home display |
| `display_undocked` | zsh alias | Switch to laptop display only |
