FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Create non-root user
RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --prefer-binary -r requirements.txt

# Copy application code
COPY . .

# Fix permissions
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["gunicorn", "app.main:app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--timeout", "60"]
