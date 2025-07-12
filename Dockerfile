FROM python:3.11-slim as base
ENV INSTALL_DEV_DEPS=${INSTALL_DEV_DEPS:-false}
WORKDIR /app
COPY pyproject.toml .
COPY --chmod=755 scripts/ ./scripts/
RUN pip install uv
RUN ./scripts/setup_venv.sh

FROM python:3.11-slim as runner
ENV INSTALL_DEV_DEPS=${INSTALL_DEV_DEPS:-false}
ENV PYTHONPATH=/app/src
WORKDIR /app
COPY --chmod=755 scripts/ ./scripts/
COPY --from=base /app/.venv/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY src/ ./src/

# TODO set up non-root user per https://archive.is/VA08q
EXPOSE 8000 5678

CMD ["./scripts/start.sh"] 