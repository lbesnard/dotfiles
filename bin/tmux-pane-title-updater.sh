#!/usr/bin/env bash
# Keeps each pane's title (#T) in sync with its running command. Runs as its
# own background loop instead of a #() job inside pane-border-format, so
# pane-border redraws don't keep firing on every bit of pane activity and
# clobbering out-of-band graphics (e.g. chafa -f kitty) drawn in the pane.
while :; do
    panes=$(tmux list-panes -a -F '#{pane_id} #{pane_tty}') || exit 0
    while read -r pane_id pane_tty; do
        cmd=$(ps -t "$pane_tty" -o args= 2>/dev/null | head -n1)
        [ -n "$cmd" ] && tmux select-pane -t "$pane_id" -T "$cmd" 2>/dev/null
    done <<< "$panes"
    sleep 1
done
