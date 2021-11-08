from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import random
import asyncio
import os

from app.aum_worker import AUMWorker

app = FastAPI()


AUM_TASK_REPEAT_TIME = int(os.environ.get("AUM_TASK_REPEAT_TIME")) or 30


@app.on_event("startup")
@repeat_every(seconds=AUM_TASK_REPEAT_TIME)
async def aum_job():
    worker = AUMWorker()
    worker.send()
