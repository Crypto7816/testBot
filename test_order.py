# # Python
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

exchange = ccxt.binanceusdm({
        'apiKey': 'f45c92ae2192b1d3ba924179699b82f4bdb6fb77aaf272131841388f80b97c90',
        'secret': '5025ce62c0e52a98dbb4e33f2786f9bb2d34df450de4ff4e2fdb7e4199dca63a',
    })
exchange.set_sandbox_mode(True)

exchange.load_markets()
# markets = pd.DataFrame(exchange.markets).T
# print(markets)
symbol = 'BTC/USDT:USDT'
amount = 0.01
price = 60200

place_delayed_order(exchange, symbol, amount, price)
place_delayed_order(exchange, 'ETH/USDT:USDT', 0.1, 3000)


# import ccxt.pro as ccxt
# from asyncio import run

# print('CCXT Version:', ccxt.__version__)

# async def main():
#     exchange = ccxt.binance({
#         'apiKey': 'f45c92ae2192b1d3ba924179699b82f4bdb6fb77aaf272131841388f80b97c90',
#         'secret': '5025ce62c0e52a98dbb4e33f2786f9bb2d34df450de4ff4e2fdb7e4199dca63a',
#         'options': {
#             'defaultType': 'swap',  # spot, margin, future, delivery
#         },
#     })
#     # or
#     # exchange = ccxt.pro.binanceusdm()
#     # or
#     # exchange = ccxt.pro.binancecoinm()
#     exchange.set_sandbox_mode(True)
#     symbol = 'BTC/USDT'
#     while True:
#         try:
#             orderbook = await exchange.watch_order_book(symbol)
#             print(exchange.iso8601(exchange.milliseconds()), exchange.id, symbol, 'ask:', orderbook['asks'][0], 'bid:', orderbook['bids'][0])
#         except Exception as e:
#             print(type(e).__name__, str(e))
#             break
#     await exchange.close()


# run(main())