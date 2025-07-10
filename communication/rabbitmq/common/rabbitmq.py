import pika

from typeguard import typechecked
import multiprocessing
from typing import Callable
import json


@typechecked
class RabbitMQClient:

    def __init__(self, **kwargs) -> None:
        self._params = pika.ConnectionParameters(**kwargs)
        self._thread: dict[str, multiprocessing.Process] = {}
    
    def publish(self, queue: str, body: dict) -> None:

        conn = pika.BlockingConnection(self._params)
        ch = conn.channel()

        ch.queue_declare(queue)
        ch.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(body)
        )

        conn.close()

    def bind_callback(self, queue: str, auto_ack: bool, callback = None):

        if queue in self._thread.keys():
            raise Exception(f"consumer alredy active: {queue}")

        self._thread[queue] = multiprocessing.Process(target=self._start_consuming, args=(queue, auto_ack, callback))
        self._thread[queue].start()

    def _start_consuming(self, queue: str, auto_ack: bool, callback: Callable):

        conn = pika.BlockingConnection(self._params)
        ch = conn.channel()

        ch.queue_declare(queue)
        ch.basic_consume(
            queue=queue,
            auto_ack=auto_ack,
            on_message_callback=callback
        )

        try:
            ch.start_consuming()
        finally:
            ch.close()
            conn.close()

    def _stop_binding(self, queue: str):
        if not self._thread:
            return
        
        if self._thread[queue].is_alive():
            self._thread[queue].terminate()
            self._thread[queue].join()

    def close(self):

        for key, value in self._thread.items():
            self._stop_binding(key)        
