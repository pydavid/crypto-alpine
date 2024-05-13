import abc


class Abstract(abc.ABC):
    @abc.abstractmethod
    def request(self, method, path, params):
        raise NotImplementedError

    @abc.abstractmethod
    def set_leverage(self, value, position, symbol, margin_coin):
        raise NotImplementedError

    @abc.abstractmethod
    def get_order_detail(self, symbol, order_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_filled_order_detail(self, symbol, order_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_current_position(self, symbol, margin_coin):
        raise NotImplementedError

    @abc.abstractmethod
    def get_historical_position(self, symbol, margin_coin, limit):
        raise NotImplementedError

    @abc.abstractmethod
    def create_order(
        self, position, symbol, price, amount, margin_coin, take_profit, stop_loss
    ):
        raise NotImplementedError
