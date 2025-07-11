# Marc Streeter Dev Backend

This is the backend service for Marc Streeter's personal website, built with FastAPI to showcase modern Python development practices and AI integration.

## Features
- **FastAPI** backend with async endpoints
- **OpenAI** integration for AI-powered responses
- **httpx** for async HTTP requests
- **pytest** for testing
- **pre-commit** hooks with **black**, **ruff**, and **ty** for code quality
- **Docker** and **Kubernetes** for containerized local development
- **Tilt** for rapid local Kubernetes workflows
- **uv** for dependency management
- **debugpy** for remote debugging support

## Prerequisites

Before setting up this service, ensure you have the following installed:

- **uv** - Fast Python package manager and installer
- **tilt** - Kubernetes development environment
- **kubectl** - Kubernetes command-line tool
- **Docker** - Container runtime
- **just** - Command runner (optional but recommended)

## Setup

1. **Set up the development environment:**
   ```sh
   just setup
   ```

2. **Create OpenAI API key secret (if using OpenAI features):**
   ```sh
   kubectl create secret generic openai-api-key --from-literal=OPENAI_API_KEY=sk-...yourkey...
   ```

3. **Start the local development environment:**
   ```sh
   just start
   ```

4. **Run tests in the live environment:**
   ```sh
   just test
   ```

## Available Commands

This project uses `just` for task automation. To see all available commands:

```sh
just
```

## About Marc Streeter

I'm Marc Streeter, a software engineer passionate about building robust, scalable, and modern applications. This backend service is part of my personal website and serves as a playground for experimenting with AI, modern Python practices, and cloud-native development.

## API Endpoints

- `GET /health` — Health check endpoint for Kubernetes probes
- `POST /openai` — Takes a prompt and returns a response from OpenAI's GPT model



## Debugging

This project includes comprehensive debugging support using debugpy for both local and remote debugging.

### Remote Debugging (Kubernetes)

 **Use VS Code remote debugging:**
   - Open the Debug panel in VS Code
   - Select "FastAPI Remote Debug (K8s)" configuration
   - Set breakpoints in your code
   - Press F5 to attach the debugger



---

Feel free to fork, contribute, or reach out if you want to connect! 