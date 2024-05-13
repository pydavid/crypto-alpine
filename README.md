# crypto-alpine

Python library for cryptocurrency trading using the most common exchanges.

## How to install

```
pip install -U crypto-alpine
```

## Documentation

1. Set environment variables

```
export API_SECRET_KEY=xxx
export API_ACCESS_KEY=yyy
export API_PASSPHRASE=zzz
```

2. Initialize

```
from alpine.exchanges import Wrapper

w = Wrapper('bitget')
```

3. Set a leverage

```
w.set_leverage(leverage, position, symbol, margin_coin)
# Example: w.set_leverage(10, "long", "FETUSDT", "usdt")
```

4. Create an order

```
w.create_order(position, symbol, price, amount, margin_coin, take_profit, stop_loss)
# Example: w.create_order("long", "FETUSDT", 2.5, 100, "usdt", 3, 2)
```

5. Get order detail

```
w.get_order_detail(symbol, order_id)
# Example: w.get_order_detail("FETUSDT", "123456")
```

6. Get current position detail

```
w.get_current_position(symbol, margin_coin)
# Example: w.get_current_position("FETUSDT", "usdt")
```

7. Get historical position detail

```
w.get_historical_position(symbol, margin_coin)
# Example: w.get_historical_position("FETUSDT", "usdt")
```

## Current supported cryptocurrency exchanges

- bitget

## Need help 

Please create an issue if you need a feature/exchange to be implemented.

## Support

If you wish to support the project:

- Ethereum: 0xf11B49666d3386C96Af1A496bFA5688c83B25E8e
- Solana: C7USpoN4kxEm81w3mpK7FuNQ7zcMWY9fqyuacPafRqnk
- Bitcoin (segwit): bc1qcq7fdn4khlsc5ldmlf0ezks8p9r5q2hn04lyy5
