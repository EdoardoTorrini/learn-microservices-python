import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from controller.date_controller import get_datetime_route
from controller.health_controller import get_heartbeat_route
from controller.metadata_controller import get_metadata_route

import os, socket, requests


@asynccontextmanager
async def lifespan(app: FastAPI):
    hostname = socket.gethostname()
    name, ip = os.getenv("CONSUL_NAME_SERVICE", "datetime-service"), socket.gethostbyname(hostname)

    payload = {
        "ID": f"{name}-{int.from_bytes(os.urandom(2), "big")}",
        "Name": name,
        "Address": ip,
        "Port": int(os.getenv("PORT", 8080)),
        "Check": {
            "HTTP": f"http://{ip}:{int(os.getenv("PORT", 8080))}/health",
            "Interval": "10s",
            "Timeout": "1s"
        },
        "Tags": [
            "traefik.enable=true",
            "traefik.http.routers.datetime.rule=PathPrefix(`/datetime`)",
            "traefik.http.routers.datetime.entrypoints=web",
            "traefik.http.services.datetime.loadbalancer.server.port=80"
        ]

    }

    try:
        req = requests.put(f"http://{os.getenv("CONSUL_HOST")}:{os.getenv("CONSUL_PORT")}/v1/agent/service/register", json=payload)
        print(f"[+] request for the registration of the {name} is {req.status_code}", flush=True)
    except Exception as e:
        print(f"[-] failed connection to consul: {str(e)}")

    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(get_datetime_route())
app.include_router(get_heartbeat_route())
app.include_router(get_metadata_route())

if __name__ == "__main__":
    ip, port = os.getenv("HOST", "0.0.0.0"), int(os.getenv("PORT", 8080))
    uvicorn.run(app, host=ip, port=port)