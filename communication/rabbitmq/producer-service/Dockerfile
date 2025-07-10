FROM rabbitmq-common
COPY ./primes /app/primes
COPY ./producer.py /app/

CMD ["python", "/app/producer.py"]