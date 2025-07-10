FROM alpine:latest

RUN apk add --no-cache python3 py3-pip \
    && ln -sf python3 /usr/bin/python

WORKDIR /app
COPY ./common /app/common

RUN python -m pip install -r /app/common/requirements.txt --break-system-packages
CMD ["python"]