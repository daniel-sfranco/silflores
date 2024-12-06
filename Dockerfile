FROM python:3.12.5-alpine3.20
LABEL maintainer="danielsfranco346@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY silfloresapp /silfloresapp
COPY scripts /scripts

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
  apk add postgresql-client

ENV PATH="/scripts:/venv/bin:$PATH"

USER root

CMD ["commands.sh"]
