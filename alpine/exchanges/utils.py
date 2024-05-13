def compute_closing(leverage, amount, symbol_value, stop, factor=1):
    """
    When a TP or SL are given as percentage of the PnL, compute it
    as the symbol's value.
    :param leverage: The leverage of the order.
    :type leverage: float
    :param amount: the amount of coin to buy.
    :type amount: float
    :param symbol_value: The initial symbol price.
    :type symbol_value: float
    :param stop: The treshold of the Pnl in percentage to stop the order.
    :type stop: str
    :param factor: The factor for the stop. -1 if it's a SL.
    :type stop: int
    :returns: The treshold to stop the order.
    :rtype: float
    """
    stop_percentage = factor * float(stop.replace("%", "")) / 100
    stop_value = (amount * symbol_value / leverage) * stop_percentage
    stop = (stop_value + amount * symbol_value) / amount
    return round(stop, 3)


def compute_amount(leverage, margin_coin, symbol_value):
    """
    Compute amount of coin to buy using the margin coin.
    :param leverage: The leverage of the order.
    :type leverage: float
    :param margin_coin: the amount of coin to buy with.
    :type margin_coin: float
    :param symbol_value: The initial symbol price.
    :type symbol_value: float
    :returns: The amount of coin to by.
    :rtype: float
    """
    amount = leverage * float(margin_coin.replace("coin", ""))
    return round(amount / symbol_value, 5)
