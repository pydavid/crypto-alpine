import importlib


class Wrapper:
    def __init__(self, exchange_name):
        """
        :param exchange_name: The exchange name to use.
        :type exchange_name: str
        """
        self.exchange_name = exchange_name
        module = importlib.import_module(f"alpine.exchanges.{exchange_name}")
        self.exchange = getattr(module, exchange_name.capitalize())()

    def set_leverage(self, value, position, symbol, margin_coin):
        """
        Set the leverage to value.
        :param value: the leverage's value.
        :type value: int
        :param position: Position's direction.
        :type position: str
        :param symbol: symbol to set the leverage for.
        :type symbol: str
        :param margin_coin: The margin coin to use for the position.
        :type margin_coin: str
        """
        return self.exchange.set_leverage(value, position, symbol, margin_coin)

    def create_order(
        self, position, symbol, price, amount, margin_coin, take_profit, stop_loss
    ):
        """
        Create an order.
        :param position: Position's direction.
        :type position: str
        :param symbol: symbol to create an order for.
        :type symbol: str
        :param price: The price of the symbol we want to fill the position at.
        :type price: None,float
        :param amount: Amount of the coin to use to open the position with.
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
        return self.exchange.create_order(
            position, symbol, price, amount, margin_coin, take_profit, stop_loss
        )

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
        return self.exchange.get_order_detail(symbol, order_id)

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
        return self.exchange.get_filled_order_detail(symbol, order_id)

    def get_current_symbol_value(self, symbol):
        """
        Retrieve the current market value of the symbol.
        :param symbol: symbol to retrieve the market's value.
        :type symbol: str
        :returns: the current symbol price.
        :rtype: float
        """
        return self.exchange.get_current_symbol_value(symbol)

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
        return self.exchange.get_current_position(symbol, margin_coin)

    def get_historical_position(self, symbol, margin_coin, limit=1):
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
        return self.exchange.get_historical_position(symbol, margin_coin, limit)

    def close_position(self, symbol, position):
        """
        Close the current position of the given the symbol.
        :param symbol: symbol to close the current position.
        :type symbol: str
        :param position: Position's direction.
        :type position: str
        :returns: None
        :rtype: None
        """
        return self.exchange.close_position(symbol, position)

    def get_account_details(self):
        """
        Get margin and equity details about the account.
        :returns: The account details.
        :rtype: dict
        """
        return self.exchange.get_account_details()
