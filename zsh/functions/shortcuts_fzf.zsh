# sk - Shortcut Finder
# Searches the shortcuts cheatsheet using fzf.
# Usage: sk [query]
# Example: sk lock screen
#          sk tmux split
function sk() {
    local shortcuts_file="${DOTFILES_PATH:-$HOME/github_repo/dotfiles}/cheat/personal/shortcuts.md"
    [[ ! -f "$shortcuts_file" ]] && shortcuts_file="$HOME/.cheat/personal/shortcuts.md"

    if [[ ! -f "$shortcuts_file" ]]; then
        echo "shortcuts.md not found. Expected at: $shortcuts_file"
        return 1
    fi

    local result
    result=$(
        grep '^|' "$shortcuts_file" \
        | grep -v '^|--' \
        | grep -v '^| Shortcut' \
        | awk -F'|' '{
            shortcut=$2; tool=$3; desc=$4;
            gsub(/^ +| +$/, "", shortcut);
            gsub(/^ +| +$/, "", tool);
            gsub(/^ +| +$/, "", desc);
            if (shortcut != "" && tool != "" && desc != "")
                printf "%-45s %-18s %s\n", shortcut, tool, desc
          }' \
        | fzf --ansi \
              --prompt='shortcut> ' \
              --header='Shortcut                                      Tool               Description' \
              --query="$*" \
              --layout=reverse \
              --preview-window=hidden
    )

    if [[ -n "$result" ]]; then
        local shortcut
        shortcut=$(echo "$result" | awk '{print $1}')
        echo "$result"
        # Copy shortcut to clipboard if xclip/xsel/wl-copy available
        if command -v xclip &>/dev/null; then
            echo -n "$shortcut" | xclip -sel clip && echo "(shortcut copied to clipboard)"
        elif command -v xsel &>/dev/null; then
            echo -n "$shortcut" | xsel --clipboard --input && echo "(shortcut copied to clipboard)"
        elif command -v wl-copy &>/dev/null; then
            echo -n "$shortcut" | wl-copy && echo "(shortcut copied to clipboard)"
        fi
    fi
}
