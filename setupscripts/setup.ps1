Write-Host "🔧 Setting up StatScience (Docker + Django)..."

# Optional: Clone repo
# git clone https://github.com/yourusername/statscience.git
# Set-Location -Path statscience

# Create .env if it doesn't exist
if (-Not (Test-Path ".env")) {
    $secret = [System.Guid]::NewGuid().ToString("N")
    @"
DJANGO_SECRET=$secret
DEBUG=True
"@ | Out-File -Encoding UTF8 .env
    Write-Host "✅ .env created."
}

# Build containers
docker-compose build

# Run migrations
docker-compose run web python manage.py migrate

# Create superuser
docker-compose run web python manage.py createsuperuser

# Start the app
docker-compose up -d

Write-Host "🚀 StatScience is running at http://localhost:8000"
