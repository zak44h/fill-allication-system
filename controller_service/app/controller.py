from typing import Dict
from collections import defaultdict
from math import ceil
import os
import requests


class Controller:
    """Controls data from fill and AUM servers, sends output information to position server"""

    def __init__(self):
        self.fills = []
        self.results = defaultdict(dict)

    async def tick_fills_handler(self, data: Dict):
        self.fills.append(data)

    async def tick_assets_handler(self, data: Dict):
        groupped_fills = defaultdict(lambda: defaultdict(int))

        # Handles stacking values of price and quantity
        # (same stock has been bought several times during fill ticks)
        for fill in self.fills:
            groupped_fills[fill["stock_ticker"]]["price"] += fill["price"]
            groupped_fills[fill["stock_ticker"]]["quantity"] += fill["quantity"]

        self.fills = []

        for ticker_name, values in groupped_fills.items():
            for account_name, percentage in data.items():
                # Do not rearrange previous trade fills
                if ticker_name not in self.results[account_name]:
                    self.results[account_name][ticker_name] = ceil(percentage / 100 * values["quantity"])

    def send(self) -> None:
        url = os.environ.get("POSITION_SERVICE_URL")
        requests.post(f"{url}/result_positions", json=self.results)
