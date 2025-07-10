import os, random, string, time
from uuid import uuid4
from datetime import datetime

from model.event import Event, EventType
from handler.event_handler import EventHandler


gen_str = lambda x: "".join([ random.choice(string.ascii_letters) for _ in range(x) ])


def main():

    handler = EventHandler(os.getenv("KAFKA_TOPIC"))
    while 1:

        event = Event(
            type=EventType.CREATE,
            key=str(uuid4()),
            data={
                "timestamp": int(datetime.now().timestamp() * 1e3),
                "username": gen_str(10),
                "email": f"{gen_str(5)}.{gen_str(5)}@gmail.com"
            }
        )

        handler.send(event)

        time.sleep(random.randint(1, 10))
    handler.flush()

if __name__ == "__main__":
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"[+] exit")