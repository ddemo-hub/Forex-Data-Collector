from src.app.base_container import BaseContainer

from src.utils.globals import Globals
from src.utils.logger import Logger

from abc import ABC, abstractmethod
import requests

class BaseCollector(ABC):
    def __init__(self, base_container: BaseContainer):
        self.config_service = base_container.config_service
        self.data_service = base_container.data_service

    def post_webhooks(self, hooks: list, timestamp: int, exchange: str, buy_sell: str, currency: str, rate: float):
        for hook in hooks:
            if currency in hook["currencies"]:
                try:
                    requests.post(url=hook, json={"timestamp": timestamp, "exchange": exchange, "buy_sell": buy_sell, currency: rate})
                except Exception as ex:
                    Logger.error(f"[{exchange}][POST] {ex}")
        
    def emit_sockets(self, exchange: str, rates: dict):
        Globals.socketio.emit("update_rates", {"exchange": exchange, "rates": rates})

    @abstractmethod
    def run(self):
        pass