
import pandas as pd
import yfinance as yf
import datetime
from datetime import date
import ta
from binance import Client
from strategy import SuperTrendStrategy as superStrat, OneminStrategy as oneStrat, Strategy as srat
from strategy import ThreeEmaStrategy as tStrat
from strategy import RideTheTrendStrategy as ride
import divergence

def testOnAll(debut,strate, devise):
    timeframe = ["5m", "15m", "30m", "1h", "4h"]
    #timeframe = ["1m"]
    gain = -100
    tMax = ""
    current = date.today().strftime("%d/%m/%Y")
    print("de", debut, "à", current)
    for t in timeframe:
        print("Backtest sur ", t)
        df = getBinanceData(devise, t, debut)
        strate.setData(df)
        strate.test(0, debut, str(current), commission=0)
        gainP = strate.getGainP()
        if(gainP > gain):
            gain = gainP
            tMax = t
        print(t, "-", gainP, "gain -", strate.getGain(), 'gag =', strate.nbGain, 'p =', strate.nbPerte, 'maxP =', strate.getMaxPerte())
        print("Total commission = ", strate.getTotalCommission())
        strate.reinitialiser()
    print("Best Pourcentage de gain = ", tMax, gain)
    
def testOnAllForex(period, devise, strate):
    timeframe = ["5m", "15m", "30m", "1h"]
    #timeframe = ["1m"]
    gain = -100
    tMax = ""
    current = date.today().strftime("%d/%m/%Y")
    print("de", period, "à", current)
    for t in timeframe:
        print("Backtest sur ", t)
        df = getForexData(devise, t, period)
        strate.setData(df)
        strate.test(0, period, str(current), commission=0)
        gainP = strate.getGainP()
        if(gainP > gain):
            gain = gainP
            tMax = t
        print(t, "-", gainP, "gain -", strate.getGain(), 'gag =', strate.nbGain, 'p =', strate.nbPerte, 'maxP =', strate.getMaxPerte())
        print("Total commission = ", strate.getTotalCommission())
        strate.reinitialiser()
    print("Best Pourcentage de gain = ", tMax, gain)

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
def getForexData(devise, interval, period):
    ok = yf.download(tickers = devise, period = period, interval = interval)
    del ok["Adj Close"]
    data = ok
    return data


s = tStrat.ThreeEmaStrategy("p")
testOnAllForex("1mo", "EURUSD=X", s)










