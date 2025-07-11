# Backend development tasks

# Default task
default:
    @just --list

# Start the backend service using Tilt
start: _check-tilt
    echo "Starting backend service with Tilt..."
    tilt up

# Setup development environment
setup:
    #!/usr/bin/env bash
    echo "Setting up backend development environment..."
    
    # Install dependencies using uv
    echo "Installing dependencies..."
    uv sync --dev
    
    # Install pre-commit hooks (activate venv first)
    echo "Installing pre-commit hooks..."
    source .venv/bin/activate && pre-commit install
    
    echo "Backend setup complete!"
    echo "Run 'just start' to start the service with Tilt"

# Run tests in the live Tilt environment
test: _check-tilt
    #!/usr/bin/env bash


    # Exec into the pod and run tests
    kubectl exec "$POD_NAME" -- python -m pytest -v

# Helper command to check if tilt is installed
_check-tilt:
    #!/usr/bin/env bash
    if ! command -v tilt &> /dev/null; then
        echo "Error: tilt is not installed. Please install tilt first."
        exit 1
    fi 