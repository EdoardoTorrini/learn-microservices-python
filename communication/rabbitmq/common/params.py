from pika import PlainCredentials
import os

ip, port = os.getenv("RABBITMQ_IP"), os.getenv("RABBITMQ_PORT")
user, pwd = os.getenv("RABBITMQ_DEFAULT_USER"), os.getenv("RABBITMQ_DEFAULT_PASS")

params = {
    "host": ip,
    "port": port,
    "credentials": PlainCredentials(user, pwd)
}