from Data import Data
from Info import Info
import pandas as pd

class Strategy:

    strategies = ["emaCrossing", "stoch_rsiEma", "threeEma", "superTrendStrategy", "adxAO"]
    def __init__(self):

        self.position = pd.Series([], dtype='float64')
        self.stoploss = pd.Series([], dtype='float64')
        self.takeprofit = pd.Series([], dtype='float64')
        self.type = pd.Series([], dtype=pd.StringDtype())

    def long(self, position, stoploss, tp):
        if stoploss <= position and tp >= position:
            self.position = self.position.append(pd.Series([position]))
            self.stoploss = self.stoploss.append(pd.Series([stoploss]))
            self.takeprofit = self.takeprofit.append(pd.Series([tp]))
            self.type = self.type.append(pd.Series(["long"]))
        else:
            print("Valeur incorrect pour le stoploss et le takeprofit")

    def short(self, position, stoploss, tp):
        if stoploss >= position and tp <= position:
            self.position = self.position.append(pd.Series([position]))
            self.stoploss = self.stoploss.append(pd.Series([stoploss]))
            self.takeprofit = self.takeprofit.append(pd.Series([tp]))
            self.type = self.type.append(pd.Series(["short"]))
        else:
            print("Valeur incorrect pour le stoploss et le takeprofit")

    def TapStopLoss(self, pos, info : Info):
        for i in range(0, len(self.stoploss)):
            if self.type.iloc[i] == "long":
                if pos <= self.stoploss.iloc[i]:
                    nb = (info.fin * info.levier)/self.position.iloc[i]
                    benef = nb * self.stoploss.iloc[i]
                    print("Stop loss long", self.stoploss.iloc[i], "perte =", benef-(info.fin*info.levier))
                    info.makeTrade(benef-(info.fin*info.levier))
                    self.stoploss.iloc[i] = -1
                    self.position.iloc[i] = -1
                    self.type.iloc[i] = -1
                    self.takeprofit.iloc[i] = -1
            elif self.type.iloc[i] == "short":
                if pos >= self.stoploss.iloc[i]:
                    nb = (info.fin * info.levier) / self.position.iloc[i]
                    benef = nb * (self.position.iloc[i] + (self.position.iloc[i] - self.stoploss.iloc[i]))
                    print("Stop loss short", self.stoploss.iloc[i], "perte =", benef-(info.fin*info.levier))
                    info.makeTrade(benef-(info.fin*info.levier))
                    self.stoploss.iloc[i] = -1
                    self.position.iloc[i] = -1
                    self.type.iloc[i] = -1
                    self.takeprofit.iloc[i] = -1

    def TapTakeProfit(self, pos, info : Info):
        for i in range(0, len(self.takeprofit)):
            if self.type.iloc[i] == "long":
                if pos >= self.takeprofit.iloc[i]:
                    nb = (info.fin * info.levier) / self.position.iloc[i]
                    benef = nb * self.takeprofit.iloc[i]
                    print("TP long", self.takeprofit.iloc[i], "gain =", benef-(info.fin*info.levier))
                    info.makeTrade(benef-(info.fin*info.levier))
                    self.stoploss.iloc[i] = -1
                    self.position.iloc[i] = -1
                    self.type.iloc[i] = -1
                    self.takeprofit.iloc[i] = -1
            elif self.type.iloc[i] == "short":
                if pos <= self.takeprofit.iloc[i]:
                    nb = (info.fin * info.levier) / self.position.iloc[i]
                    benef = nb * (self.position.iloc[i] + (self.position.iloc[i] - self.takeprofit.iloc[i]))
                    print("TP Short", self.takeprofit.iloc[i], "gain =", benef-(info.fin*info.levier))
                    info.makeTrade(benef-(info.fin*info.levier))
                    self.stoploss.iloc[i] = -1
                    self.position.iloc[i] = -1
                    self.type.iloc[i] = -1
                    self.takeprofit.iloc[i] = -1

    def emaCrossing(self, data : Data, info : Info):
        ema_25 = data.ema(25)
        ema_50 = data.ema(50)
        close = data.getClose()
        margeP = 1
        margeG = 2
        for i in range(0,len(close)):
            price = float(close.iloc[i])
            e25 = float(ema_25.iloc[i])
            e50 = float(ema_50.iloc[i])
            self.TapStopLoss(price, info)
            self.TapTakeProfit(price, info)
            if i > 50:
                if float(close.iloc[i-1]) < float(ema_25.iloc[i-1]) and float(price) >= float(e25):
                    self.long(price, price * (1 - (margeP/100)), price * (1 + (margeG/100)))
                if float(close.iloc[i-1]) > float(ema_25.iloc[i-1]) and float(price) <= float(e25):
                    self.short(price, price * (1 + (margeP/100)), price * (1 - (margeG/100)))

    def stoch_rsiEma(self, data : Data, info : Info):
        ema_200 = data.ema(200)
        stoch_rsi = data.stoch_Rsi()
        close = data.getClose()
        margeP = 0.1
        margeG = 0.2
        for i in range(0, len(close)):
            price = float(close.iloc[i])
            e200 = float(ema_200.iloc[i])
            sto = float(stoch_rsi.iloc[i])
            self.TapStopLoss(price, info)
            self.TapTakeProfit(price, info)
            if i > 200:
                if float(price) > float(e200) and float(sto) < 20 and float(close.iloc[i-1]) < float(ema_200.iloc[i-1]):
                    self.long(price, price * (1 - (margeP/100)), price * (1 + (margeG/100)))
                if float(price) < float(e200) and float(sto) > 80 and float(close.iloc[i-1]) > float(ema_200.iloc[i-1]):
                    self.short(price, price * (1 + (margeP / 100)), price * (1 - (margeG / 100)))

    def threeEma(self, data : Data, info : Info):
        ema_5 = data.ema(5)
        ema_21 = data.ema(21)
        ema_63 = data.ema(63)
        close = data.getClose()
        flag_long = False
        flag_short = False
        margeP = 0.1
        margeG = 0.2

        for i in range(0, len(close)):
            price = close.iloc[i]
            short = ema_5.iloc[i]
            middle = ema_21.iloc[i]
            long = ema_63.iloc[i]
            self.TapStopLoss(price, info)
            self.TapTakeProfit(price, info)
            if middle < long and short < middle and flag_long == False and flag_short == False:
                self.long(price, price * (1 - (margeP/100)), price * (1 + (margeG/100)))
                flag_short = True
            elif flag_short == True and short > middle:
                self.short(price, price * (1 + (margeP / 100)), price * (1 - (margeG / 100)))
                flag_short = False
    def superTrendStrategy(self, data : Data, info : Info):
        superTrend = data.supertrend(10, 1)
        ema200 = data.ema(200)
        stoch_rsi = data.stoch_Rsi()
        close = data.getClose()
        margeP = 0.1
        margeG = 0.2

        for i in range(0, len(close)):
            price = close.iloc[i]
            e200 = ema200.iloc[i]
            sto = float(stoch_rsi.iloc[i])
            avant = superTrend.iloc[i-1, 1]
            apres = superTrend.iloc[i, 1]
            self.TapStopLoss(price, info)
            self.TapTakeProfit(price, info)
            if float(avant) == -1 and float(apres) == 1 and price > e200 and float(sto) < 20:
                self.long(price, price * (1 - (margeP / 100)), price * (1 + (margeG / 100)))
            if float(avant)==1 and float(apres)==-1 and price < e200 and float(sto) > 80:
                self.short(price, price * (1 + (margeP / 100)), price * (1 - (margeG / 100)))

    def adxAO(self, data : Data, info : Info):
        ema5 = data.ema(5)
        ema50 = data.ema(50)
        ema21 = data.ema(21)
        ema200 = data.ema(200)
        bbb = data.BBB()
        adx = data.adx()
        ao = data.awesomeOscillator()
        close = data.getClose()
        margeP = 2
        margeG = 1
        for i in range(0, len(close)):
            e5 = ema5.iloc[i]
            ave5 = ema5.iloc[i-1]
            e21 = ema21.iloc[i]
            ave21 = ema21.iloc[i - 1]
            e50 = ema50.iloc[i]
            ave50 = ema50.iloc[i - 1]
            e200 = ema200.iloc[i]
            ave200 = ema200.iloc[i - 1]
            bb = bbb.iloc[i]
            aoo = ao.iloc[i]
            adxx = adx.iloc[i]
            price = close.iloc[i]

            self.TapStopLoss(price, info)
            self.TapTakeProfit(price, info)
            if ave5 < ave21 and e5 >= e21 and ave50 < ave200 and e50 >= e200 and bb > 0.75 and adxx > 15 and aoo > 2 and price > e5:
                self.long(price, price * (1 - (margeP / 100)), price * (1 + (margeG / 100)))
            if ave5 > ave21 and e5 <= e21 and ave50 > ave200 and e50 <= e200 and bb < 0.15 and adxx > 15 and aoo < 2 and price < e5:
                self.short(price, price * (1 + (margeP / 100)), price * (1 - (margeG / 100)))





