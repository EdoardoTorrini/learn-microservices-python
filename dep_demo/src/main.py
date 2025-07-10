import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from user.user_service import UserService
from user.user_controller import get_user_route

import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(get_user_route())

if __name__ == "__main__":
    ip, port = os.getenv("IP"), int(os.getenv("PORT"))
    uvicorn.run(app, host=ip, port=port)