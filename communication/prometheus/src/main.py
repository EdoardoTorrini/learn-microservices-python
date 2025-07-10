from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from stresser.stress_view import get_stress_route

import os, uvicorn


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

Instrumentator().instrument(app).expose(app)

app.include_router(get_stress_route())
ip, port = os.getenv("HOST"), int(os.getenv("PORT"))


if __name__ == "__main__":
    uvicorn.run(app, host=ip, port=port)
