import os


class Config:

    ip = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8080"))

    ip_time = os.getenv("IP_TIME", "172.20.6.10")
    port_time = os.getenv("PORT_TIME", 8000)
    url_time = f"http://{ip_time}:{port_time}/time"