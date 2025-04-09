FROM python:3.10-alpine3.16

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt
COPY app/ /app
COPY ./scripts /scripts

WORKDIR /app

RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    pip install -r /requirements.txt && \
    apk del .tmp-deps 

RUN adduser --disabled-password --no-create-home django && \
    mkdir -p /vol/static && \
    mkdir -p /vol/media && \
    chown -R django:django /vol && \
    chown -R django:django /app && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER django

CMD ["run.sh"]
