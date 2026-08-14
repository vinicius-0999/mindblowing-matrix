#!/usr/bin/env bash
set -e

rm -f "/tmp/.X${DISPLAY#:}-lock"
Xvfb "$DISPLAY" -screen 0 1280x800x24 -ac &
XVFB_PID=$!
sleep 1

fluxbox &
x11vnc -display "$DISPLAY" -nopw -forever -shared -rfbport 5900 -quiet &
websockify --web=/usr/share/novnc 6080 localhost:5900 &

trap 'kill $XVFB_PID 2>/dev/null' EXIT
exec python main.py
