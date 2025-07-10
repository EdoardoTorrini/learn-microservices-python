from confluent_kafka import Producer, Message, KafkaError
from model.event import Event
import os, socket, json


class EventHandler(Producer):

    _res = {}

    def __init__(self, topic: str) -> None:
        conf = {
            "bootstrap.servers": f"{os.getenv("KAFKA_HOST")}:{os.getenv("KAFKA_PORT")}",
            "client.id": socket.gethostname()
        }
        super().__init__(conf)

        self._topic = topic

    def ack(self, err: KafkaError, msg: Message):
        key = msg.key().decode() if msg.key() else "None"
        if key in self._res.keys():
            self._res[key] = err

        self._res[key] = 0 if err is not None else -1
    
    def send(self, msg: Event):
        if not isinstance(msg, Event):
            raise AttributeError()
        
        self.produce(self._topic, key=str(msg.key), value=json.dumps(msg.model_dump()).encode(), callback=self.ack)
        self._res[str(msg.key)] = None
        self.poll(0)
