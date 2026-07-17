#!/bin/bash
set -e

echo "Starting Sales KPI backend..."

PORT="${PORT:-8000}"
if [ "${DEV:-0}" = "1" ]; then
  exec uvicorn main:app --host 0.0.0.0 --port "$PORT" --reload
else
  exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
fi
