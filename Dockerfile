# Dashboard Logística Loggi - Dockerfile
# Build profissional para produção

FROM python:3.11-slim-bookworm AS base

WORKDIR /app

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# =============================================================================
# Builder image para develop-eggs
# =============================================================================
FROM base AS builder

WORKDIR /app

COPY . .

# Instalar dependências de desenvolvimento
RUN pip install -e ".[dev]"

# =============================================================================
# Production image
# =============================================================================
FROM base AS production

WORKDIR /app

# Criar usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash appuser

# Copiar apenas o necessário para produção
COPY --from=builder /app/src ./src
COPY --from=builder /app/assets ./assets
COPY --from=builder /app/docs ./docs

# Dar permissão ao usuário não-root
RUN chown -R appuser:appuser /app
USER appuser

# Expor porta
EXPOSE 8050

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8050/', timeout=5)" || exit 1

# Command para produção com gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8050", "-w", "4", "-t", "120", "src.app:server"]