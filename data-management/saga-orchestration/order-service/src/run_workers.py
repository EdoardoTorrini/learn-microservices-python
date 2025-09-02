# run_workers.py
import logging
from conductor.client.configuration.configuration import Configuration
from conductor.client.automator.task_handler import TaskHandler

import order.workers  # noqa: F401  # importa per registrare i @worker_task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("run_workers")
    cfg = Configuration()  # legge CONDUCTOR_SERVER_URL dall'env

    handler = TaskHandler(
        configuration=cfg,
        scan_for_annotated_workers=True,
        import_modules=["order.workers"],  # dove stanno i worker
        # process_count=1,        # opzionale
        # polling_interval=100,   # opzionale (ms)
        # domain="dev",           # opzionale se usi i domain
    )
    handler.start_processes()   # <-- niente 'block='

if __name__ == "__main__":
    main()
