#!/bin/bash

# DramaBench Local Server Launcher
# Opens the demo in browser with a local HTTP server

cd "$(dirname "$0")"

echo "🚀 Starting DramaBench Web Demo..."
echo "📂 Server running at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Try to open in default browser
if command -v open &> /dev/null; then
    # macOS
    sleep 1 && open http://localhost:8000 &
elif command -v xdg-open &> /dev/null; then
    # Linux
    sleep 1 && xdg-open http://localhost:8000 &
elif command -v start &> /dev/null; then
    # Windows
    sleep 1 && start http://localhost:8000 &
fi

# Start Python HTTP server
if command -v uv &> /dev/null; then
    uv run python -m http.server 8000
else
    python3 -m http.server 8000
fi
