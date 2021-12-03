import pandas as pd
import yfinance as yf
import datetime
from datetime import date
import ta
from binance import Client


class Data:

    def __init__(self):
        self.high = pd.Series([], dtype='float64')
        self.low = pd.Series([], dtype='float64')
        self.close = pd.Series([], dtype='float64')
        self.volume = pd.Series([], dtype='float64')
        self.indicators = pd.DataFrame

    def getBinanceData(self, devise, timeframe, debut):
        try:
            klinesT = Client().get_historical_klines(devise, timeframe, debut)
            df = pd.DataFrame(klinesT,
                              columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av',
                                       'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
            self.close = df['close']
            self.low = df['low']
            self.high = df['high']
            self.volume = df['volume']
        except Exception as e:
            print(format(e))

    def getForexData(self, devise, period, interval):
        try:
            df = yf.download(tickers=devise, period=period, interval=interval)
            self.close = df['Adj Close']
            self.low = df['Low']
            self.high = df['High']
            self.volume = df['Volume']
        except Exception as e:
            print(format(e))

    def getLow(self) -> pd.Series:
        return self.low

    def getClose(self) -> pd.Series:
        return self.close

    def getVolume(self) -> pd.Series:
        return self.volume

    def getIndicators(self) -> pd.DataFrame:
        return self.indicators

    def getIndicator(self, name) -> pd.Series:
        return self.indicators[name]

    def ema(self, value):
        try:
            ema = ta.trend.ema_indicator(self.close, value)
        except Exception as e:
            print(format(e))
        return ema

    def sma(self, value):
        try:
            return ta.trend.sma_indicator(self.close, value)
        except Exception as e:
            print(format(e))