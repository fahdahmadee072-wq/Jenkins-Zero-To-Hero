FROM python:3.11-slim AS builder

WORKDIR /app

# Install system updates (fix OS vulnerabilities)
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade pip tools (fix vulnerabilities)
RUN pip install --upgrade pip setuptools wheel

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir prometheus-flask-exporter

# ------------------------

FROM python:3.11-slim

WORKDIR /app

# Create non-root user (VERY IMPORTANT)
RUN useradd -m appuser

# Copy installed packages
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app
COPY app.py .

# Change ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

ENV PORT=5000

EXPOSE 5000

CMD ["gunicorn", "--preload", "app:app", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-"]
