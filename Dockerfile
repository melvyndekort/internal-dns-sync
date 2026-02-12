FROM python:3.15.0a6-alpine3.22 AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk add --no-cache git openssh-client && \
    python -m venv /venv

ENV PATH="/venv/bin:$PATH"


FROM base AS build

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY internal_dns_sync/ ./internal_dns_sync/
RUN uv build --wheel && pip install dist/*.whl


FROM python:3.15.0a6-alpine3.22 AS runtime

LABEL org.opencontainers.image.source=https://github.com/melvyndekort/internal-dns-sync

RUN apk add --no-cache git openssh-client

COPY --from=build /venv /venv

ENV PATH="/venv/bin:$PATH"

CMD ["python3", "-m", "internal_dns_sync.main"]
