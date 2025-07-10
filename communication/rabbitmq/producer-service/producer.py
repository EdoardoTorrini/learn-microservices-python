from common.rabbitmq import RabbitMQClient
from common.event import Event, EventType
from common.params import params

from primes.primes_controller import get_prime_route
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

import string, random, time
from uuid import uuid4

import multiprocessing
import uvicorn, os


def main():

    print(f"{params = }")
    client = RabbitMQClient(**params)
    gen_str = lambda x: "".join([ random.choice(string.ascii_letters) for _ in range(x) ])

    while 1:
        event = Event[str, dict](
            type=EventType.CREATE,
            key=str(uuid4()),
            data={"username": gen_str(7), "email": f"{gen_str(7)}@gmail.com"}
        )

        client.publish("basic", dict(event))

        time.sleep(random.randint(1, 10))

    client.close()

if __name__ == "__main__":

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"]
    )

    app.include_router(get_prime_route())
    ip, port = os.getenv("HOST"), int(os.getenv("PORT"))

    try:
        thread = multiprocessing.Process(target=main, args=())
        thread.start()

        uvicorn.run(app, host=ip, port=port)
    except KeyboardInterrupt:
        thread.terminate()
        thread.join()