#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

/cloud-sql-proxy silflores:southamerica-east1:silflores-postgres --address 127.0.0.1 &

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

python manage.py makemigrations --noinput
python manage.py collectstatic --noinput

echo "Listing contents of /silfloresapp/static/dist:"
ls -lR /silfloresapp/static/dist

echo "Listing contents of /silfloresapp/static/img:"
ls -lR /silfloresapp/static/img

echo "Listing contents of /data/web/static:"
ls -lR /data/web/static
daphne silflores.asgi:application --bind 0.0.0.0 --port 8000
