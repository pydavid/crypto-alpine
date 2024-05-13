import hashlib
import hmac
import os
import requests
import sys
import time
import urllib.parse
from . import Abstract


class Binance(Abstract):
    API_ENDPOINT = "https://fapi.binance.com"

    def _signature(self, params):
        """
         HTTP Calls needs a specific signature.
        :param params: The HTTP parameters.
         :type params: dict
        """
        return hmac.new(
            os.environ.get("API_SECRET_KEY").encode("utf-8"),
            params.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def request(self, method, path, params):
        """
        HTTP Call to the API.
        :param method: The HTTP method. POST or GET.
        :type method: str
        :param path: The HTTP path.
        :type path: str
        :param params: The HTTP parameters.
        :type params: dict
        """
        path_query = urllib.parse.urlencode(params, True).replace("%40", "@")
        payload = {
            "signature": self._signature(path_query),
            "timestamp": int(time.time() * 1000),
            "params": path_query,
        }
        headers = {
            "X-MBX-APIKEY": os.environ.get("API_ACCESS_KEY"),
        }
        r = requests.request(
            method, f"{self.API_ENDPOINT}{path}", json=payload, headers=headers
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            print(r.text)
            sys.exit(1)

    def set_leverage(self, value, position, symbol):
        """
        Set the leverage to value.
        :param value: the leverage's value.
        :type value: int
        :param position: Position's direction.
        :type position: str
        :param symbol: symbol to set the leverage for.
        :type symbol: str
        """
        return self.request(
            "POST",
            "/fapi/v1/leverage",
            {"symbol": symbol, "leverage": value},
        )

    def create_order(
        self, position, symbol, price, amount, margin_coin, take_profit, stop_loss
    ):
        pass
