import random
import requests
import os


class FillWorker:
    """Prepares and sends data to controller server"""

    # Price and quantity are random but have a range limit
    # For output convinience

    SERVICE = "fill"
    STOCKS = ("Amazon", "Berkshire Hathaway", "Apple", "Facebook", "JPMorgan Chase",
              "Johnshon & Johnson", "Tesla", "Visa", "AXA", "Microsoft")

    def __init__(self):
        self.data = {
            "stock_ticker": self.STOCKS[random.randint(0, 9)],
            "price": self._get_price(),
            "quantity": self._get_quantity()
        }

    @staticmethod
    def _get_price() -> int:
        return random.randint(1, 100)

    @staticmethod
    def _get_quantity() -> int:
        return random.randint(1, 50)

    def send(self) -> None:
        url = os.environ.get("CONTROLLER_SERVICE_URL")
        requests.post(f"{url}/submit/{self.SERVICE}", json=self.data)
