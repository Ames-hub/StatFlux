# Use slim Python image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python statscience/manage.py collectstatic --noinput

# Use gunicorn/uvicorn to serve Django
CMD ["uvicorn", "statscience.statscience.asgi:application", "--host", "0.0.0.0", "--port", "3000"]

EXPOSE 2030