FROM alpine:latest

RUN apk add --no-cache \
    python3 \
    py3-pip \
    gcc \
    musl-dev \
    git \
    bash \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cmake \
    make \
    g++ && ln -sf python3 /usr/bin/python

WORKDIR /app
COPY . /app/

RUN cd /tmp && git clone https://github.com/confluentinc/librdkafka.git && cd librdkafka \
    git checkout v2.10.1 > /dev/null && ./configure && make -j$(nproc) && make install

RUN python -m pip install -r /app/requirements.txt --break-system-packages
CMD ["python", "/app/main.py"]
