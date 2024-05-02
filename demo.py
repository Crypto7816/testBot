import asyncio
from tardis_client import TardisClient, Channel
from typing import TypedDict, Literal
import pandas as pd
from tqdm.asyncio import tqdm
from configparser import ConfigParser

config = ConfigParser()
config.read('./.config/config.cfg')

API_KEY = config.get('Tardis', 'apiKey')

class Exchange:
    SUPPORTED_EXCHANGES = Literal[
        'bitmex',
        'deribit',
        'binance-futures', # binance-usdt-futures
        'binance-delivery', # binance-coin-futures
        'binance', # binance-spot
        'ftx', 
        'okex-futures', # okx-futures
        'okex-swap', # okx-swap
        'okex-options', # okx-options
        'okex', # okx-spot
        'huobi-dm', # huobi-futures
        'huobi-dm-swap', # huobi-coin-swap
        'huobi-dm-linear-swap', # huobi-usdt-swap
        'huobi', # huobi Gobal
        'bitfinex-derivatives', # bitfinex-derivatives
        'bitfinex',
        'coinbase',
        'cryptofacilities',
        'kraken',
        'bitstamp',
        'gemini',
        'bybit',
        'bybit-spot',
        'dydx',
        'woo-x',
        'kucoin',
        'blockchain-com',
        'upbit',
        'phemex',
        'delta',
        'ascendex',
        'ftx-us',
        'binance-us',
        'gate-io-futures',
        'gate-io',
        'bitnomial',
        'crypto-com',
        'okcoin'
    ]
    
    def __init__(self, name: SUPPORTED_EXCHANGES, api_key: str):
        self.name = name
        self.api_key = api_key
    


    






async def replay():
    tardis_client = TardisClient(api_key=API_KEY)

    # replay method returns Async Generator
    # https://rickyhan.com/jekyll/update/2018/01/27/python36.html
    messages = tardis_client.replay(
        exchange="binance-futures",
        from_date="2020-02-01",
        to_date="2020-02-02",
        filters=[Channel(name='ticker',symbols=["btcusdt"])]
    )

    # create an empty list to store the data
    data = []

    # this will print all trades and orderBookL2 messages for XBTUSD
    # and all trades for ETHUSD for bitmex exchange
    # between 2019-06-01T00:00:00.000Z and 2019-06-02T00:00:00.000Z (whole first day of June 2019)
    async for local_timestamp, message in tqdm(messages):
        # local timestamp is a Python datetime that marks timestamp when given message has been received
        # message is a message object as provided by exchange real-time stream
        
        res = message['data']
        time = res['E']
        last = res['c'] # close
        open = res['o']
        high = res['h']
        low = res['l']
        volume = res['v']
        
        # append the data to the list
        data.append([time, last, open, high, low, volume])
        # print(f"Time: {time}, Last: {last}, Open: {open}, High: {high}, Low: {low}, Volume: {volume}")
    # create a pandas DataFrame from the list of data
    df = pd.DataFrame(data, columns=['Time', 'Last', 'Open', 'High', 'Low', 'Volume'])
    
    # print the DataFrame
    print(df)

asyncio.run(replay())