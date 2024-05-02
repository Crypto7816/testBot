# Python
import ccxt.pro
import asyncio
from asyncio import run, gather
from pprint import pprint
from ccxt.pro import exchanges
from configparser import ConfigParser

config = ConfigParser()
config.read('./.config/config.cfg')

API_KEY = config.get('binance-test', 'apiKey')
API_SECRET = config.get('binance-test', 'secret')

async def place_delayed_order(exchange: ccxt.pro.Exchange, symbol, amount, price):
    try:
        order = await exchange.create_order(symbol, 'limit', 'buy', amount, price)
        print(exchange.iso8601(exchange.milliseconds()), 'place_delayed_order')
        pprint(order)
        print('---------------------------------------------------------------')
    except Exception as e:
        # break
        print(e)

async def watch_orders_loop(exchange, symbol):
    while True:
        try:
            orders = await exchange.watch_orders(symbol)
            for order in orders:
                if order['status'] == 'open' and order['filled'] == 0:
                    print('---------------------------Open Order NEW---------------------------')
                    pprint(order)
                elif order['status'] == 'open' and order['filled'] == 0:
                    print('---------------------------Open Order PARTIALLY FILLED---------------------------')
                    pprint(order)
                elif order['status'] == 'closed':
                    print('---------------------------Close Order---------------------------')
                    pprint(order)
                elif order['status'] == 'canceled':
                    print('---------------------------Cancel Order---------------------------')
                    pprint(order)
            # print(exchange.iso8601(exchange.milliseconds()), 'watch_orders_loop', len(orders), ' last orders cached')
            print('---------------------------------------------------------------')
        except Exception as e:
            # break
            print(e)


async def watch_balance_loop(exchange):
    while True:
        try:
            balance = await exchange.watch_balance()
            print(exchange.iso8601(exchange.milliseconds()), 'watch_balance_loop')
            pprint(balance)
            print('---------------------------------------------------------------')
        except Exception as e:
            # break
            print(e)

async def watch_positions_loop(exchange:ccxt.Exchange):
    while True:
        try:
            positions = await exchange.fetch_positions()
            print(exchange.iso8601(exchange.milliseconds()), 'watch_positions_loop')
            pprint(positions)
            print('---------------------------------------------------------------')
            await asyncio.sleep(1)
        except Exception as e:
            # break
            print(e)

orderbooks = {}

def print_orderbook(exchange: ccxt.Exchange, symbol, orderbook, limit: int = 5):
    # this is a common handler function
    # it is called when any of the orderbook is updated
    # it has access to both the orderbook that was updated
    # as well as the rest of the orderbooks
    # ...................................................................
    print('-------------------------------------------------------------')
    print('Last updated:', exchange.iso8601(exchange.milliseconds()))
    # ...................................................................
    # print just one orderbook here
    # print(orderbook['datetime'], symbol, orderbook['asks'][0], orderbook['bids'][0])
    # ...................................................................
    # or print all orderbooks that have been already subscribed-to
    for symbol, orderbook in orderbooks.items():
        print(orderbook['datetime'], symbol, orderbook['asks'][:limit], orderbook['bids'][:limit])
        
async def watch_orderbook_loop(exchange: ccxt.Exchange, symbol):
    # a call cost of 1 in the queue of subscriptions
    # means one subscription per exchange.rateLimit milliseconds
    your_delay = 1
    await exchange.throttle(your_delay)
    while True:
        try:
            orderbook = await exchange.watch_order_book(symbol)
            orderbooks[symbol] = orderbook
            print_orderbook(exchange, symbol, orderbook)
        except Exception as e:
            print(type(e).__name__, str(e))


async def watch_orderbooks_loop(exchange: ccxt.Exchange, symbol_list):
    loops = [watch_orderbook_loop(exchange, symbol) for symbol in symbol_list]
    # let them run, don't for all tasks cause they execute asynchronously
    # don't print here
    await asyncio.gather(*loops)



async def main():
    exchange = ccxt.pro.binanceusdm({
        'apiKey': API_KEY,
        'secret': API_SECRET,
    })
    exchange.set_sandbox_mode(True)
    symbol_1 = 'BTC/USDT:USDT'
    symbol_2 = 'ETH/USDT:USDT'
    amount = 0.01
    price = 62000
    loops = [
        watch_orderbooks_loop(exchange, symbol_list=[symbol_1, symbol_2]),
        # watch_orders_loop(exchange, symbol_1),
        # watch_balance_loop(exchange),
        # watch_positions_loop(exchange),
        # place_delayed_order(exchange, symbol, amount, price)
    ]
    await gather(*loops)
    await exchange.close()


run(main())
# import ccxt.pro as ccxtpro
# from asyncio import get_event_loop, ensure_future
# from pprint import pprint


# print('CCXT Pro Version:', ccxtpro.__version__)


# class MyBinance(ccxtpro.binance):
#     def on_connected(self, client, message=None):
#         print('Connected to', client.url)
#         ensure_future(create_order(self))

#     async def on_partially_filled_order(self, client, order):
#         print('--------------------------------------------------------------')
#         print('Partially Filled Order:')
#         pprint(order)

#     async def on_filled_order(self, client, order):
#         print('--------------------------------------------------------------')
#         print('Filled Order:') 
#         pprint(order)

#     async def on_canceled_order(self, client, order):
#         print('--------------------------------------------------------------')
#         print('Canceled Order:')
#         pprint(order)


# async def create_order(exchange):
#     symbol = 'BTC/USDT'
#     type = 'limit'
#     side = 'buy'
#     amount = 123.45  # change for your values
#     price = 54.321  # change for your values
#     params = {}
#     try:
#         order = await exchange.create_order(symbol, type, side, amount, price, params)
#         print('--------------------------------------------------------------')
#         print('create_order():')
#         pprint(order)
#     except Exception as e:
#         print(type(e).__name__, str(e))


# async def watch_orders(exchange):
#     while True:
#         try:
#             orders = await exchange.watch_orders()
#             for order in orders:
#                 if order['status'] == 'open':
#                     await exchange.on_partially_filled_order(exchange, order)
#                 elif order['status'] == 'closed':
#                     if order['filled'] == order['amount']:
#                         await exchange.on_filled_order(exchange, order)
#                     else:
#                         await exchange.on_canceled_order(exchange, order)
#         except Exception as e:
#             print(type(e).__name__, str(e))
#             break
#     await exchange.close()


# loop = get_event_loop()
# exchange = MyBinance({
#     'enableRateLimit': True,
#     'apiKey': 'YOUR_API_KEY',
#     'secret': 'YOUR_SECRET',
#     'asyncio_loop': loop,
# })

# loop.run_until_complete(watch_orders(exchange))