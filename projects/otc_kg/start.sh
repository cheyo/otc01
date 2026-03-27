#!/bin/bash
echo "Starting OTC KG Backend..."
cd /root/.openclaw/workspace/projects/otc_kg/backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
echo "Backend started on http://localhost:8000"
echo ""
echo "To view frontend, open: /root/.openclaw/workspace/projects/otc_kg/frontend/index.html"
