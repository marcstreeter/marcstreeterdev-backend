#!/bin/bash

# Smart startup script for FastAPI backend
# Handles both production and development modes with debugpy support

set -e

# Default values
DEBUGPY_ENABLED=${DEBUGPY_ENABLED:-"false"}
DEBUGPY_WAIT=${DEBUGPY_WAIT:-"false"}
DEBUGPY_PORT=${DEBUGPY_PORT:-"5678"}
INSTALL_DEV_DEPS=${INSTALL_DEV_DEPS:-"false"}
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-"8000"}

# Activate virtual environment if it exists (for local development)
if [ -f ".venv/bin/activate" ]; then
    echo "🔧 Activating virtual environment..."
    source .venv/bin/activate
fi

echo "🚀 Starting FastAPI backend..."
echo "   Host: $HOST"
echo "   Port: $PORT"
echo "   Dev Dependencies: $INSTALL_DEV_DEPS"
echo "   Debugpy Enabled: $DEBUGPY_ENABLED"
echo "   Debugpy Wait: $DEBUGPY_WAIT"

# Check if we should use debugpy
if [ "$INSTALL_DEV_DEPS" = "true" ]; then
    if [ "$DEBUGPY_ENABLED" = "true" ]; then
        echo "🔧 Starting with debugpy support on port $DEBUGPY_PORT"
        DEBUGPY_ARGS="--listen 0.0.0.0:$DEBUGPY_PORT"
        if [ "$DEBUGPY_WAIT" = "true" ]; then
            DEBUGPY_ARGS="$DEBUGPY_ARGS --wait"
        fi
        
        echo "🔧 Debugpy args: $DEBUGPY_ARGS"
        echo "🔧 Full command: python -Xfrozen_modules=off -m debugpy $DEBUGPY_ARGS -m uvicorn src.main:app --host $HOST --port $PORT --reload"
        
        # Start with debugpy
        exec python -Xfrozen_modules=off -m debugpy $DEBUGPY_ARGS -m uvicorn src.main:app --host $HOST --port $PORT --reload
    else
        echo "⚠️  Debugpy available but not used. Starting without debugpy."
        exec python -m uvicorn src.main:app --host $HOST --port $PORT --reload
    fi
else
    echo "🏭 Starting in production mode"
    exec python -m uvicorn src.main:app --host $HOST --port $PORT --reload
fi 