from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import random
import asyncio
import os

from app.fill_worker import FillWorker

app = FastAPI()

MAX_FILL_SERVICE_SLEEP_TIME = int(os.environ.get("MAX_FILL_SERVICE_SLEEP_TIME")) or 30
MAX_WORKERS_PER_TICK = int(os.environ.get("MAX_WORKERS_PER_TICK")) or 10
FILL_TASK_REPEAT_TIME = int(os.environ.get("FILL_TASK_REPEAT_TIME")) or 3


@app.on_event("startup")
@repeat_every(seconds=FILL_TASK_REPEAT_TIME)
async def fill_job():
    # Tries to simulate `X number of fill servers` part
    # Number of workers (servers) is generated randomly at each function call
    for _ in range(random.randint(1, MAX_WORKERS_PER_TICK)):
        worker = FillWorker()
        worker.send()

    await asyncio.sleep(random.randint(1, MAX_FILL_SERVICE_SLEEP_TIME))
