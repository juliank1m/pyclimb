# PyClimb Django Application
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files at build time (doesn't need database)
# Set minimal env vars needed for collectstatic to run
RUN SECRET_KEY=build-only-key DEBUG=false python manage.py collectstatic --noinput --clear

# Note: Migrations run via Procfile release command, NOT during build
# The database isn't available at build time

# Run gunicorn (Railway provides PORT via environment variable)
CMD ["sh", "-c", "gunicorn pyclimb.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
