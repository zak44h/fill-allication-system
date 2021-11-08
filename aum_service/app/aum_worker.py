from typing import List
import random
import os
import requests


class AUMWorker:
    """Prepares and sends AUM data to controller server"""

    SERVICE = "aum"

    def __init__(self):
        self.data = {}

        for index, value in enumerate(self._get_percentages(), start=1):
            self.data[f"Account{index}"] = value

    @staticmethod
    def _get_percentages() -> List[int]:
        result = []
        value = 100

        while value > 0:
            percentage = random.randint(1, value)
            value -= percentage
            result.append(percentage)

        return result

    def send(self) -> None:
        url = os.environ.get("CONTROLLER_SERVICE_URL")
        requests.post(f"{url}/submit/{self.SERVICE}", json=self.data)
