#!/bin/bash
# Start local static server for glukhova-dasha.com
# ES modules require HTTP (file:// won't work)

PORT=${1:-8080}
echo "Starting server on http://localhost:$PORT"
echo "Open http://localhost:$PORT/index.html"
python3 -m http.server "$PORT"
