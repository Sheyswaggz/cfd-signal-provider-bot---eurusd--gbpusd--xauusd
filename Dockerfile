FROM python:3.11-slim

LABEL maintainer="Trading Bot Team"
LABEL version="0.1.0"
LABEL description="CFD Signal Provider Bot for EURUSD, GBPUSD, XAUUSD"

WORKDIR /app

RUN groupadd -r appgroup && useradd -r -g appgroup -u 1000 appuser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

USER appuser

EXPOSE ${PORT}

HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:${PORT}/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:application"]