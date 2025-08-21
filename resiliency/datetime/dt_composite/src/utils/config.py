import os


class Config:

    ip = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8080"))

    ip_sim = os.getenv("IP_SIM", "172.20.6.10")
    port_sim = os.getenv("PORT_SIM", 8000)
    url_time = f"http://{ip_sim}:{port_sim}/time"
    url_date = f"http://{ip_sim}:{port_sim}/date"