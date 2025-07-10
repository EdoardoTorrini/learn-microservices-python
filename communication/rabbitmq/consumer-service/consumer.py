from common.rabbitmq import RabbitMQClient
from common.event import Event
from common.params import params

import json, sympy


def rabbitmq_basic(ch, method, properties, body):
    event = Event(**json.loads(body))
    print(f"[+] receive: {event}", flush=True)


def rabbitmq_cpu_intensive(ch, method, properties, body):
    event, keys = Event[str, dict](**json.loads(body)), ["lower_bound", "upper_bound", "email"]
    
    if not isinstance(event.data, dict):
        raise TypeError(f"body of event must be dict, type: {type(event.data)}")
    
    if not all(key in event.data.keys() for key in keys):
        raise KeyError(f"miss some parameter for this call, it needs {keys}")
    
    ret = [ sympy.nextprime(event.data.get("lower_bound")) ]
    while ret[-1] < event.data.get("upper_bound"):
        ret.append(sympy.nextprime(ret[-1]))
    
    print(f"[+] prime: {ret}", flush=True)

def main():

    client = RabbitMQClient(**params)
    
    client.bind_callback(
        queue="basic",
        auto_ack=True,
        callback=rabbitmq_basic
    )
    print(f"[+] create bind_callback for queue basic", flush=True)

    client.bind_callback(
        queue="cpu-intensive",
        auto_ack=True,
        callback=rabbitmq_cpu_intensive
    )
    print(f"[+] create bind_callback for queue cpu-intensive", flush=True)

    try:
        print(f"[+] waiting for message", flush=True)
        while 1:
            pass

    except KeyboardInterrupt:
        print(f"exit", flush=True)

    client.close()

if __name__ == "__main__":
    main()