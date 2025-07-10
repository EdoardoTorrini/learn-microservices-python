import os, json

from model.event import Event, EventType
from handler.event_handler import EventHandler


def main():

    consumer = EventHandler(os.getenv("KAFKA_TOPIC"))
    while 1:
        msg = consumer.poll(1.0)
        
        if msg is None or msg.error():
            continue
        
        event = Event(**json.loads(msg.value().decode()))
        print(f"{event}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"[+] exit")
