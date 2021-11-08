from typing import Dict
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import asyncio


app = FastAPI()


@app.post("/result_positions")
def result_positions_get(payload: Dict):
    for k, v in payload.items():
        print(f"Account: {k} \nValues:\n ")
        for subkey, subvalue in v.items():
            print(f"{subkey}: {subvalue}")
        print("\n")

    return {}
