#!/bin/bash
echo '=== OTC service status ==='
echo '[backend]'
ps -ef | grep "uvicorn app.main:app --host 0.0.0.0 --port 8000" | grep -v grep || echo 'not running'
echo '[frontend]'
ps -ef | grep "python3 -m http.server 8080 --bind 0.0.0.0 --directory /root/.openclaw/workspace/projects/otc_kg/frontend" | grep -v grep || echo 'not running'
echo '[health]'
curl -s http://127.0.0.1:8000/health || echo 'backend unreachable'
echo
echo '[graph]'
curl -s http://127.0.0.1:8000/graph/overview?limit=5 | head -c 300 || echo 'graph unreachable'
echo
