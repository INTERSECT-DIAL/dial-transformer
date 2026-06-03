# see https://docs.astral.sh/uv/guides/integration/docker/

FROM --platform=$BUILDPLATFORM ghcr.io/astral-sh/uv:debian-slim AS builder

ARG PYTHON_VERSION=3.12
ARG UV_NO_DEV="1"

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed
ENV UV_NO_DEV=${UV_NO_DEV}

RUN uv python install ${PYTHON_VERSION}

WORKDIR /app

# Install dependencies first for better layer caching.
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --no-install-project --no-editable

# Sync project source.
COPY src ./src
RUN uv sync --locked --no-editable

FROM --platform=$BUILDPLATFORM gcr.io/distroless/python3-debian12:nonroot AS runner

WORKDIR /app

COPY --from=builder /python /python
COPY --from=builder /app/.venv /app/.venv
COPY --chown=nonroot:nonroot local-conf.docker.json /app/local-conf.docker.json

ENV PATH="/app/.venv/bin:$PATH"
ENV DIAL_TRANSFORMER_CONFIG_FILE=/app/local-conf.docker.json

CMD ["python", "-m", "intersect_dial_transformer"]