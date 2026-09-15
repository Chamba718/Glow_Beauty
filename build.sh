#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Intentar crear el superusuario si se proveen las variables de entorno
if [[ -n "${DJANGO_SUPERUSER_USERNAME}" && -n "${DJANGO_SUPERUSER_PASSWORD}" ]]; then
  python manage.py createsuperuser --noinput || true
fi
