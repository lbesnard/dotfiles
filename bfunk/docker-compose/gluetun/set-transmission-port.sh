#!/bin/sh
# wait a few seconds for Transmission RPC
sleep 5

SID=$(curl -sI http://127.0.0.1:9091/transmission/rpc | awk '/X-Transmission-Session-Id/ {print $2}')
curl -s -H "X-Transmission-Session-Id: $SID" \
  -X POST http://127.0.0.1:9091/transmission/rpc \
  -d "{\"method\":\"session-set\",\"arguments\":{\"peer-port\":${1},\"peer-port-random-on-start\":false}}"
