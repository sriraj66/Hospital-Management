#!/bin/sh

# Exit script if any command fails
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput


# Create Django admin superuser if not already exists
echo "Creating Django admin superuser..."
DJANGO_SUPERUSER_PASSWORD=admin  # Set your desired superuser password here
DJANGO_SUPERUSER_USERNAME=admin     # Set your desired superuser username here
DJANGO_SUPERUSER_EMAIL=admin@gmail.com  # Set your desired superuser email here
echo "from django.contrib.auth.models import User; User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell || true

# Start the Django development server
echo "Starting Django development server..."
exec "$@"
