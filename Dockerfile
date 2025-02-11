FROM python:3.12.5-alpine3.20
LABEL maintainer="danielsfranco346@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY silfloresapp /silfloresapp
COPY scripts /scripts
COPY --from=redis:7-alpine3.20 /usr/local/bin/redis-cli /usr/local/bin/redis-cli

WORKDIR /silfloresapp

EXPOSE 8080

RUN python -m venv /venv
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install -r /silfloresapp/requirements.txt
RUN adduser --disabled-password --no-create-home duser
RUN mkdir -p /data/web/static
RUN mkdir -p /data/web/media
RUN chown -R duser:duser /venv
RUN chown -R duser:duser /data/web/static
RUN chown -R duser:duser /data/web/media
RUN chmod -R 755 /data/web/static
RUN chmod -R 755 /data/web/media
RUN chmod -R +x /scripts
RUN apk add postgresql-client

ENV PATH="/scripts:/venv/bin:$PATH"

ENV REDIS_URL=redis://redis:6379/1

USER root

CMD ["commands.sh"]
