#!/bin/bash
# Display profile picker for i3 + dmenu, built on autorandr.
# Profiles live in ~/.config/autorandr (dotfiles: config/autorandr).
# Save a new one with:  autorandr --save <name>   (e.g. work, home)
# Profiles are matched by monitor EDID, so port names (DP-1-3...) don't matter.

# Two layouts: laptop only, or dual monitor. "auto" re-detects from what is plugged in.
chosen=$(printf 'auto\nlaptop\ndual\n' | dmenu -i -p display) || exit 0

case "$chosen" in
    auto) autorandr --change --force ;;
    laptop|dual) autorandr --load "$chosen" --force ;;
    *) exit 0 ;;
esac
# autorandr runs the postswitch hook itself.
