from src.app.base_container import BaseContainer

from src.utils.globals import Globals
from src.utils.logger import Logger

from abc import ABC, abstractmethod
import requests

class BaseCollector(ABC):
    def __init__(self, exchange, base_container: BaseContainer):
        self.exchange = exchange
        self.config_service = base_container.config_service
        self.data_service = base_container.data_service

    def check_response(self, response: requests.models.Response):
        if response.status_code != 200:
            Logger.error(f"[{self.exchange}] Status Code: {response.status_code}")

    def post_webhooks(self, hooks: list, timestamp: int, buy_sell: str, currency: str, rate: float):
        for hook in hooks:
            if currency in hook["currencies"]:
                try:
                    requests.post(url=hook, json={"timestamp": timestamp, "buy_sell": buy_sell, currency: rate})
                except Exception as ex:
                    Logger.error(f"[{self.exchange}][POST WEBHOOK] {ex}")
        
    def emit_sockets(self, rates: dict):
        try:
            Logger.print(f"[INFO] Emitting {'exchange': self.exchange, 'rates': rates}")
            Globals.socketio.emit("update_rates", {"exchange": self.exchange, "rates": rates})
        except Exception as ex:
            Logger.error(f"[{self.exchange}][EMIT WEBSOCKET] {ex}")
    
    
    @abstractmethod
    def run(self):
        pass