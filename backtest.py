import pandas as pd
import datetime
import ta
from binance import Client
from strategy import Strategy as strat

def reglageData(df):
    del df['close_time']
    del df['quote_av'] 
    del df['trades']
    del df['tb_base_av']
    del df['tb_quote_av']
    del df['ignore']
    for col in df.columns:
        df[col] = pd.to_numeric(df[col])
    df = df.set_index(df['timestamp'])
    df.index = pd.to_datetime(df.index, unit='ms')
    del df['timestamp']
    return df

def getBinanceData(devise, plage, debut):
    klinesT = Client().get_historical_klines(devise, plage, debut)
    df = pd.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    df = reglageData(df)
    return df

df = getBinanceData("ETHUSDT", "1h", "01 October 2021")

strat = strat.Strategy(df)
strat.addIndicator("sma_200")
strat.addIndicator("ema_50")
strat.addIndicator("macd")
strat.addIndicator("rsi") 



print(df[:100])

