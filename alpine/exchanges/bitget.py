import base64
import hmac
import json
import os
import time
import requests
import sys
import urllib.parse
from . import Abstract


class Bitget(Abstract):
    API_ENDPOINT = "https://api.bitget.com"

    def _signature(self, timestamp, method, path, params):
        """
        HTTP Calls needs a specific signature.
        :param timestamp: timestamp to use for the signature
        :type timestamp: int
        :param method: The HTTP method. POST or GET.
        :type method: str
        :param path: The HTTP path.
        :type path: str
        :param params: The HTTP parameters.
        :type params: dict
        """
        if method == "POST":
            pre_hash = f"{timestamp}{method}{path}{json.dumps(params)}"
        else:
            pre_hash = f"{timestamp}{method}{path}?{urllib.parse.urlencode(params)}"
        mac = hmac.new(
            bytes(os.environ.get("API_SECRET_KEY"), encoding="utf8"),
            bytes(pre_hash, encoding="utf-8"),
            digestmod="sha256",
        )
        return base64.b64encode(mac.digest())

    def request(self, method, path, params):
        """
        HTTP Call to the API.
        :param method: The HTTP method. POST or GET.
        :type method: str
        :param path: The HTTP path.
        :type path: str
        :param params: The HTTP parameters.
        :type params: dict
        :param json: The HTTP body.
        :type params: dict
        """
        timestamp = int(time.time() * 1000)
        params = (
            dict(sorted(params.items())) if params else None
        )  # We need to sort the dictionnary ASC
        headers = {
            "ACCESS-KEY": os.environ.get("API_ACCESS_KEY"),
            "ACCESS-SIGN": self._signature(timestamp, method, path, params),
            "ACCESS-TIMESTAMP": str(timestamp),
            "ACCESS-PASSPHRASE": os.environ.get("API_PASSPHRASE"),
            "locale": "en-US",
        }

        kwargs = {"params": params} if method == "GET" else {"json": params}
        r = requests.request(
            method, f"{self.API_ENDPOINT}{path}", headers=headers, **kwargs
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            print(f"[{method}]{self.API_ENDPOINT}{path}: {r.json()}")
            sys.exit(1)
        return r.json()

    def set_leverage(self, value, position, symbol, margin_coin):
        """
        Set the leverage to value.
        :param value: the leverage's value.
        :type value: int
        :param position: Position's direction.
        :type position: str
        :param margin_coin: The margin coin to use for the position.
        :type margin_coin: str
        :param symbol: symbol to set the leverage for.
        :type symbol: str
        :returns: None
        :rtype: None
        """
        product_type = "USDT-FUTURES"
        return self.request(
            "POST",
            "/api/v2/mix/account/set-leverage",
            {
                "symbol": symbol,
                "productType": product_type,
                "marginCoin": margin_coin,
                "leverage": value,
                "holdSide": position,
            },
        )

    def create_order(
        self, position, symbol, price, amount, margin_coin, take_profit, stop_loss
    ):
        """
        Create an order.
        :param position: Position's direction.
        :type position: str
        :param symbol: symbol to create an order for.
        :type symbol: str
        :param price: The price of the symbol we want to fill the order at.
        :type price: None,float
        :param amount: Amount of the coin to use to open the order with.
        :type amount: float
        :param margin_coin: The margin coin to use.
        :type margin_coin: str
        :param take_profit: The symbol's price at which we close the order.
        :type take_profit: float
        :param stop_loss: The symbol's price at which we exit the order.
        :type stop_loss: float
        :returns: the order id.
        :rtype: str
        """
        product_type = "USDT-FUTURES"
        margin_mode = "isolated"
        trade_side = "open"
        side = "buy" if position == "long" else "sell"
        return self.request(
            "POST",
            "/api/v2/mix/order/place-order",
            {
                "symbol": symbol,
                "productType": product_type,
                "marginCoin": margin_coin,
                "marginMode": margin_mode,
                "size": amount,
                "price": price,
                "side": side,
                "tradeSide": trade_side,
                "orderType": "limit" if price else "market",
                # "presetStopSurplusPrice": take_profit,
                # "presetStopLossPrice": stop_loss,
            },
        )["data"]["orderId"]

    def get_order_detail(self, symbol, order_id):
        """
        Get details about an order.
        :param symbol: symbol to create an order for.
        :type symbol: str
        :param order_id: the order ID to check.
        :type order_id: str
        :returns: the order details.
        :rtype: dict
        """
        product_type = "USDT-FUTURES"
        return self.request(
            "GET",
            "/api/v2/mix/order/detail",
            {
                "symbol": symbol,
                "productType": product_type,
                "orderId": order_id,
            },
        )["data"]

    def get_filled_order_detail(self, symbol, order_id):
        """
        Get details about a filled order.
        :param symbol: symbol to check the filled order for.
        :type symbol: str
        :param order_id: the order ID to check.
        :type order_id: str
        :returns: the order details.
        :rtype: dict
        """
        product_type = "USDT-FUTURES"
        return self.request(
            "GET",
            "/api/v2/mix/order/fills",
            {
                "symbol": symbol,
                "productType": product_type,
                "orderId": order_id,
            },
        )["data"]

    def get_current_position(self, symbol, margin_coin):
        """
        Retrieve the current position of the given the symbol.
        :param symbol: symbol to retrieve the current position.
        :type symbol: str
        :param margin_coin: The margin coin used for the symbol.
        :type margin_coin: str
        :returns: the position details.
        :rtype: dict
        """
        product_type = "USDT-FUTURES"
        result = self.request(
            "GET",
            "/api/v2/mix/position/single-position",
            {
                "symbol": symbol,
                "productType": product_type,
                "marginCoin": margin_coin,
            },
        )["data"]
        return result[0] if result else None

    def get_historical_position(self, symbol, margin_coin, limit):
        """
        Retrieve the historical position of the given the symbol.
        :param symbol: symbol to retrieve the historical position.
        :type symbol: str
        :param margin_coin: The margin coin used for the symbol.
        :type margin_coin: str
        :param limit: The limit of historical positions to retrieve for the symbol.
        :type limit: int
        :returns: the position details.
        :rtype: dict
        """
        product_type = "USDT-FUTURES"
        result = self.request(
            "GET",
            "/api/v2/mix/position/history-position",
            {
                "symbol": symbol,
                "productType": product_type,
                "marginCoin": margin_coin,
                "limit": limit,
            },
        )["data"]["list"]
        return result[0] if result else None

    def get_current_symbol_value(self, symbol, index="markPrice"):
        """
        Retrieve the current market value of the symbol.
        :param symbol: symbol to retrieve the market's value.
        :type symbol: str
        :param index: The index of the price to return. Default to `markPrice`.
        :type index: str
        :returns: the current price.
        :rtype: str
        """
        product_type = "USDT-FUTURES"
        result = self.request(
            "GET",
            "/api/v2/mix/market/symbol-price",
            {
                "symbol": symbol,
                "productType": product_type,
            },
        )["data"]
        return float(result[0][index])
