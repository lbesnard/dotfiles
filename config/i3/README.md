# i3 shortcuts & bar clicks

`$mod` = Super (Mod4). Config: `config`. Bar: i3blocks (`../i3blocks/config`, scripts in `../i3blocks/scripts/`).
Reload `$mod+Shift+c` · Restart `$mod+Shift+r` (also reloads the bar).

## Launch

| Keys | Action |
|---|---|
| `$mod+Return` | Terminal (ghostty, fallback i3-sensible-terminal) |
| `$mod+Shift+Return` | App launcher (i3-dmenu-desktop) |
| `$mod+w` | Firefox |
| `$mod+t` | pcmanfm |
| `$mod+Shift+k` | Passhole (password only) |
| `$mod+Shift+u` | Passhole (user + tab + password) |
| `$mod+Shift+l` | Lock screen (blur) |
| `$mod+p` | Display layout menu |
| `Print` | Screenshot (scrot) to `~/Pictures` |
| `$mod+Shift+e` | Exit i3 (asks to confirm) |

## Windows

| Keys | Action |
|---|---|
| `$mod+q` | Close window |
| `$mod+h/j/k/l` or arrows | Focus left/down/up/right |
| `$mod+Shift+h/j` or `$mod+Shift+arrows` | Move window (`Shift+k` is taken by passhole, use `Shift+Up`) |
| `$mod+z` / `$mod+v` | Next split horizontal / vertical |
| `$mod+f` | Fullscreen |
| `$mod+s` | Stacking layout |
| `$mod+e` | Toggle split layout |
| `$mod+Shift+space` | Toggle floating |
| `$mod+space` | Switch focus tiling/floating |
| `$mod+a` | Focus parent |
| `$mod+r` | Resize mode: `h/j/k/l` or arrows, `Enter`/`Esc` to leave |
| `$mod+Left mouse drag` | Move floating window |

## Workspaces

| Keys | Action |
|---|---|
| `$mod+1..0` | Go to workspace 1–10 |
| `$mod+Shift+1..0` | Move window to workspace |

Auto-assigned: Firefox → 3, pcmanfm → 4, VirtualBox → 5, Zoom → 5 (floating, main window tiled).

## Media keys

| Key | Action |
|---|---|
| `XF86AudioRaise/LowerVolume` | Volume ±2% (bar updates instantly) |
| `XF86AudioMute` | Mute toggle |
| `XF86MonBrightnessUp/Down` | Brightness ±5% |

## Bar: mouse actions

Left = button 1, middle = 2, right = 3, wheel up/down = 4/5. A dash means nothing happens.

| Block | Left | Middle | Right | Wheel |
|---|---|---|---|---|
| Battery | – | – | – | – |
| Bandwidth | – | – | – | – |
| IP (private) | – | – | Copy public IP to clipboard | – |
| Wi-Fi | Pick network (rofi + nmcli; asks password for new secured networks) | Wi-Fi radio on/off | nm-connection-editor | – |
| VPN (bfunk, UTAS) | – | – | – | – |
| CPU | Open btop/htop/top | – | – | – |
| Disk | – | – | – | – |
| Memory | – | – | – | – |
| Temperature | – | – | – | – |
| Volume | Mute toggle | pavucontrol | Choose output device (rofi) | Volume ±2% |
| Brightness | – | – | – | Brightness ±5% |
| Date | Toggle calendar popup | – | – | – |
| Power icon | Menu: lock, suspend, hibernate, logout, reboot, shutdown (any button; confirms logout/reboot/shutdown) | same | same | – |

Colours: CPU, Disk and Memory fade green → yellow → red with usage (`../i3blocks/scripts/lib.sh`).
Battery turns red ≤15% and green while charging; temperature turns orange ≥75°C and red ≥90°C.

## Tray

Tray (nm-applet, blueman, CopyQ) shows on the primary output only (`tray_output primary`).
Autostart: nm-applet, blueman-applet, copyq, Nextcloud (`--background`), Joplin, mouse button map.
Note: `exec` lines only run at login, not on `$mod+Shift+r`.
