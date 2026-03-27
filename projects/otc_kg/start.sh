#!/bin/bash
set -e
ROOT=/root/.openclaw/workspace/projects/otc_kg
mkdir -p /tmp

# kill old listeners safely
pkill -f "python3 -m http.server 8080 --bind 0.0.0.0 --directory $ROOT/frontend" 2>/dev/null || true
pkill -f "uvicorn app.main:app --host 0.0.0.0 --port 8000" 2>/dev/null || true
sleep 1

nohup bash -lc "cd $ROOT/backend && uvicorn app.main:app --host 0.0.0.0 --port 8000" >/tmp/otc_backend.log 2>&1 &
echo $! >/tmp/otc_backend.pid

nohup python3 -m http.server 8080 --bind 0.0.0.0 --directory "$ROOT/frontend" >/tmp/otc_frontend.log 2>&1 &
echo $! >/tmp/otc_frontend.pid

sleep 3
echo "Backend PID: $(cat /tmp/otc_backend.pid)"
echo "Frontend PID: $(cat /tmp/otc_frontend.pid)"
echo "Health: $(curl -s http://127.0.0.1:8000/health || echo fail)"
echo "Front: $(curl -I -s http://127.0.0.1:8080 | head -1 || echo fail)"
