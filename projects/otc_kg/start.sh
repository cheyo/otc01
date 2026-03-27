#!/bin/bash
set -e
ROOT=/root/.openclaw/workspace/projects/otc_kg
BACKEND_PID_FILE=/tmp/otc_backend.pid
FRONTEND_PID_FILE=/tmp/otc_frontend.pid

mkdir -p /tmp

# stop old
if [ -f "$BACKEND_PID_FILE" ] && kill -0 $(cat "$BACKEND_PID_FILE") 2>/dev/null; then kill $(cat "$BACKEND_PID_FILE") || true; fi
if [ -f "$FRONTEND_PID_FILE" ] && kill -0 $(cat "$FRONTEND_PID_FILE") 2>/dev/null; then kill $(cat "$FRONTEND_PID_FILE") || true; fi
pkill -f "uvicorn app.main:app --host 0.0.0.0 --port 8000" 2>/dev/null || true
pkill -f "http.server 8080 --bind 0.0.0.0" 2>/dev/null || true

cd "$ROOT/backend"
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 >/tmp/otc_backend.log 2>&1 &
echo $! > "$BACKEND_PID_FILE"

cd "$ROOT/frontend"
nohup python3 -m http.server 8080 --bind 0.0.0.0 >/tmp/otc_frontend.log 2>&1 &
echo $! > "$FRONTEND_PID_FILE"

echo "Backend:  http://0.0.0.0:8000"
echo "Frontend: http://0.0.0.0:8080"
echo "Backend PID: $(cat $BACKEND_PID_FILE)"
echo "Frontend PID: $(cat $FRONTEND_PID_FILE)"
