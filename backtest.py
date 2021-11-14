import pandas as pd
import ta
from binance import Client

from strategy import Strategy as strat

klinesT = Client().get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "01 October 2021")
df = pd.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])


del df['close_time']
del df['quote_av'] 
del df['trades']
del df['tb_base_av']
del df['tb_quote_av']
del df['ignore']



for col in df.columns:
    df[col] = pd.to_numeric(df[col])

strat = strat.Strategy(df)
strat.addIndicator("sma_200")
strat.addIndicator("ema_50")
strat.addIndicator("macd")
strat.addIndicator("rsi") 



print(df)