FROM node:alpine as frontend-builder

WORKDIR /app

COPY package.json .
COPY package-lock.json .
RUN npm install

# Copy the entire silfloresapp directory
COPY silfloresapp /app/silfloresapp
COPY vite.config.js /app/vite.config.js

# Run Vite build, using the config file
RUN npm run build -- --config /app/vite.config.js

# Debugging commands in frontend-builder stage
RUN echo "Contents of /app/silfloresapp/static/ after Vite build:" && ls -l /app/silfloresapp/static/ &&     echo "Contents of /app/silfloresapp/static/dist/ after Vite build:" && ls -l /app/silfloresapp/static/dist/

FROM python:alpine3.21

LABEL maintainer="danielsfranco346@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY silfloresapp /silfloresapp
COPY scripts /scripts
COPY --from=redis:7-alpine3.20 /usr/local/bin/redis-cli /usr/local/bin/redis-cli
COPY silflores-proxy-key.json /silflores-proxy-key.json
COPY cloud-sql-proxy /cloud-sql-proxy

WORKDIR /silfloresapp

EXPOSE 8000

RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /silfloresapp/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  mkdir -p /data/web/static && \
  mkdir -p /data/web/media && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /data/web/static && \
  chown -R duser:duser /data/web/media && \
  chmod -R 755 /data/web/static && \
  chmod -R 755 /data/web/media && \
  chmod -R +x /scripts && \
  apk add postgresql-client && \
  apk add --no-cache curl && \
  apk add --no-cache \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont && \
  rm -rf /var/cache/apk/* && \
  curl -o /cloud_sql_proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.6.1/cloud-sql-proxy.linux.amd64 && \
  chmod +x /cloud_sql_proxy

# Copy built frontend assets from the frontend-builder stage
COPY --from=frontend-builder /app/silfloresapp/static/dist /silfloresapp/static/dist

ENV PATH="/scripts:/venv/bin:$PATH"

USER root

RUN python manage.py collectstatic --noinput

CMD ["commands.sh"]
