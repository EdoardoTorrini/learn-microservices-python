FROM alpine:latest

RUN apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    gcc \
    musl-dev \
    mariadb-dev \
    pkgconfig \
    && ln -sf python3 /usr/bin/python

WORKDIR /app
COPY ./src /app

RUN python3 -m pip install -r /app/requirements.txt --break-system-packages
CMD ["/usr/bin/python", "/app/main.py"]