#!/usr/bin/env bash
# Usage: pactl_volume.sh +2% | -2% | M     (PipeWire via wpctl)
S=@DEFAULT_AUDIO_SINK@
case "$1" in
  M) wpctl set-mute $S toggle ;;
  +*) wpctl set-volume -l 1.0 $S "${1#+}+" ;;
  -*) wpctl set-volume $S "${1#-}-" ;;
esac
pkill -RTMIN+1 i3blocks
