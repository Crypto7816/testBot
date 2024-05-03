import pandas as pd

class Ticker:
    def __init__(
        self,
        base: str,
        quote: str,
        last: float,
        high: float,
        low: float,
        close: float,
        open: float,
        settlement: str = None,
        ask: float = None,
        askVolume: float = None,
        average: float = None,
        baseVolume: float = None,
        change: float = None,
        datatime: str = None,
        percentage: float = None,
        previousClose: float = None,
        quoteVolume: float = None,
        timestamp: int = None,
        vwap: float = None,
        info: dict = None
    ):
        if settlement is not None:
            self.symbol = f"{base}/{quote}:{settlement}"
        else:
            self.symbol = f"{base}/{quote}"
        self._base = base
        self._quote = quote
        self._settlement = settlement
        self.last = last
        self.high = high
        self.low = low
        self.close = close
        self.open = open
        self.ask = ask
        self.askVolume = askVolume
        self.average = average
        self.baseVolume = baseVolume
        self.change = change
        self.datatime = pd.to_datetime(datatime)
        self.percentage = percentage
        self.previousClose = previousClose
        self.quoteVolume = quoteVolume
        self.timestamp = timestamp
        self.vwap = vwap
        self.info = info
        

class Order:
    def __init__(self):
        pass