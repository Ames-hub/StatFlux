#!/bin/bash
set -e

echo "🔧 Setting up StatScience (Docker + Django)..."

# Clone your repo (optional - remove if already inside)
# git clone https://github.com/yourusername/statscience.git
# cd statscience

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "DJANGO_SECRET_KEY=$(openssl rand -hex 32)" > .env
    echo "DEBUG=False" >> .env
    echo "✅ .env created."
fi

# Build Docker containers
docker-compose build

# Run migrations
docker-compose run web python manage.py migrate

# Create superuser
docker-compose run web python manage.py createsuperuser

# Start everything
docker-compose up -d

echo "🚀 StatScience is running at http://localhost:8000"