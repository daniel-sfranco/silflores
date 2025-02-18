#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

/cloud-sql-proxy silflores:southamerica-east1:silflores-postgres --address 0.0.0.0 &

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

python manage.py makemigrations --noinput
python manage.py migrate --noinput
daphne silflores.asgi:application --bind 0.0.0.0 --port 8000
