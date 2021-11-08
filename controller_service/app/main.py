from typing import Dict
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import random
import asyncio
import os

from app.controller import Controller


app = FastAPI()
controller = Controller()

CONTROLLER_TASK_REPEAT_TIME = int(os.environ.get("CONTROLLER_TASK_REPEAT_TIME")) or 10


@app.post("/submit/{service}")
async def controller_service_post(service: str, payload: Dict):
    if service == "fill":
        await controller.tick_fills_handler(payload)
    elif service == "aum":
        await controller.tick_assets_handler(payload)

    return {}


@app.on_event("startup")
@repeat_every(seconds=CONTROLLER_TASK_REPEAT_TIME)
async def controller_send_info_job():
    controller.send()
