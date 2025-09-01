import os


class Config:

    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", 8080)