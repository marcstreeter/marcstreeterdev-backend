FROM python:3.11-slim as base
ARG INSTALL_DEV_DEPS=false
ENV INSTALL_DEV_DEPS=$INSTALL_DEV_DEPS
WORKDIR /app
COPY pyproject.toml .
COPY scripts/ ./scripts/
RUN chmod +x scripts/setup_venv.sh
RUN pip install uv
RUN ./scripts/setup_venv.sh

FROM python:3.11-slim as runner
ARG INSTALL_DEV_DEPS=false
ENV INSTALL_DEV_DEPS=$INSTALL_DEV_DEPS
WORKDIR /app
ENV PYTHONPATH=/app/src
COPY --from=base /app/.venv/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY src/ ./src/
COPY scripts/ ./scripts/
RUN chmod +x scripts/start.sh

# Switch to python user (default for python images)
USER python

EXPOSE 8000 5678

CMD ["./scripts/start.sh"] 