#!/bin/sh
set -e

echo "Starting Sales KPI frontend (Vite)..."
exec npm run dev -- --host 0.0.0.0 --port 5173
