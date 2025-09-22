FROM alpine:latest

RUN apk add --no-cache python3 py3-pip \
    && ln -sf python3 /usr/bin/python

WORKDIR /app
COPY ./src /app/

RUN python -m pip install -r /app/requirements.txt --break-system-packages
CMD ["python", "/app/main.py"]