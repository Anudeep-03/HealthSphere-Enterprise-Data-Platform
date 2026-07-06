# Build Stage
FROM python:3.12-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final Stage
FROM python:3.12-slim

WORKDIR /app

# Create non-root user for security
RUN groupadd -r healthsphere && useradd -r -g healthsphere healthsphere

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R healthsphere:healthsphere /app

USER healthsphere

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
