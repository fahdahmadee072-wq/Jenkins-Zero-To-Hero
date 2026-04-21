FROM python:3.11-slim AS builder

WORKDIR /app

# Install system deps (NO upgrade)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install Python dependencies (single layer, no cache)
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------

FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m appuser

# Copy installed packages
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app
COPY app.py .

# Set ownership
RUN chown -R appuser:appuser /app

USER appuser

ENV PORT=5000

EXPOSE 5000

CMD ["gunicorn", "--preload", "app:app", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-"]
INVALIDINSTRUCTION test
