# Shared helpers: source with  . "$(dirname "$0")/lib.sh"
# pct_color N -> hex colour fading green (0) -> yellow (50) -> red (100)
pct_color() {
  local p=$1 r g
  [ "$p" -lt 0 ] && p=0; [ "$p" -gt 100 ] && p=100
  if [ "$p" -le 50 ]; then r=$(( 80 + 175*p/50 )); g=250
  else r=255; g=$(( 250 - 165*(p-50)/50 )); fi
  printf '#%02x%02x%02x' "$r" "$g" 107
}
