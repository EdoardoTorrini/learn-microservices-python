from confluent_kafka import Consumer, KafkaError
from model.event import Event
import os, socket, json

import multiprocessing


class EventHandler(Consumer):

    _res = {}

    def __init__(self, topic: str) -> None:
        conf = {
            "bootstrap.servers": f"{os.getenv("KAFKA_HOST")}:{os.getenv("KAFKA_PORT")}",
            "group.id": f"group.id-{os.urandom(4).hex()}",
            'auto.offset.reset': 'earliest'
        }
        super().__init__(conf)

        self.subscribe([topic])
        print(f"successful listening on topic: {topic}")
