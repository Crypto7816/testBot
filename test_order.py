# Python
import ccxt
import pandas as pd
from pprint import pprint

def place_delayed_order(exchange: ccxt.Exchange, symbol, amount, price):
    try:
        order = exchange.create_order(symbol, 'limit', 'buy', amount, price)
        print(exchange.iso8601(exchange.milliseconds()), 'place_delayed_order')
        print('---------------------------------------------------------------')
    except Exception as e:
        # break
        print(e)

exchange = ccxt.binancecoinm({
        'apiKey': 'f45c92ae2192b1d3ba924179699b82f4bdb6fb77aaf272131841388f80b97c90',
        'secret': '5025ce62c0e52a98dbb4e33f2786f9bb2d34df450de4ff4e2fdb7e4199dca63a',
    })
exchange.set_sandbox_mode(True)

exchange.load_markets()
markets = pd.DataFrame(exchange.markets).T
print(markets)
symbol = 'BTC/USDT:USDT'
amount = 0.01
price = 60200

place_delayed_order(exchange, symbol, amount, price)

