# Dashboard Logística - imagem de produção
FROM python:3.11-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DASH_HOST=0.0.0.0 \
    DASH_PORT=8050

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src ./src
COPY assets ./assets
COPY main.py .

RUN useradd --create-home --shell /bin/bash appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8050

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8050/', timeout=5)" || exit 1

# waitress já está em requirements.txt (antes: gunicorn ausente e `src.app:server` inexistente)
CMD ["waitress-serve", "--host=0.0.0.0", "--port=8050", "src.wsgi:server"]
