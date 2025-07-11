#!/bin/bash

# Script to set up virtual environment based on environment variables
# Usage: ./scripts/setup_venv.sh
# Environment variables:
#   - INSTALL_DEV_DEPS: if set to "true", installs dev dependencies
#   - VENV_PATH: path to create virtual environment (default: .venv)

set -e

# Default virtual environment path
VENV_PATH=${VENV_PATH:-".venv"}

echo "Setting up virtual environment at: $VENV_PATH"

# Remove existing venv if it exists
if [ -d "$VENV_PATH" ]; then
    echo "Removing existing virtual environment..."
    rm -rf "$VENV_PATH"
fi

# Create new virtual environment
echo "Creating new virtual environment..."
uv venv "$VENV_PATH"

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Install dependencies based on environment
if [ "${INSTALL_DEV_DEPS:-false}" = "true" ]; then
    echo "Installing main dependencies + dev dependencies..."
    uv pip install -e ".[dev]"
else
    echo "Installing main dependencies only..."
    uv pip install -e .
fi

echo "Virtual environment setup complete!"
echo "Virtual environment location: $VENV_PATH"
echo "To activate: source $VENV_PATH/bin/activate" 