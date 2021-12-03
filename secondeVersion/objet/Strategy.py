from Data import Data
from Info import Info
import pandas as pd

class Strategy:

    strategies = ["emaCrossing"]
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
                    perte = self.position.iloc[i] - self.stoploss.iloc[i]
                    info.makeTrade(-perte)
                    print("Stop loss ", self.stoploss.iloc[i], "perte =", -perte)
                    self.stoploss.iloc[i] = -1
                    self.position.iloc[i] = -1
                    self.type.iloc[i] = -1
                    self.takeprofit.iloc[i] = -1
            elif self.type.iloc[i] == "short":
                if pos >= self.stoploss.iloc[i]:
                    perte = self.stoploss.iloc[i] - self.position.iloc[i]
                    print("Stop loss ", self.stoploss.iloc[i], "perte =", -perte)
                    info.makeTrade(-perte)
                    self.stoploss.iloc[i] = -1
                    self.position.iloc[i] = -1
                    self.type.iloc[i] = -1
                    self.takeprofit.iloc[i] = -1

    def TapTakeProfit(self, pos, info : Info):
        for i in range(0, len(self.takeprofit)):
            if self.type.iloc[i] == "long":
                if pos >= self.takeprofit.iloc[i]:
                    perte = self.takeprofit.iloc[i] - self.position.iloc[i]
                    info.makeTrade(perte)
                    print("TP ", self.takeprofit.iloc[i], "gain =", perte)
                    self.stoploss.iloc[i] = -1
                    self.position.iloc[i] = -1
                    self.type.iloc[i] = -1
                    self.takeprofit.iloc[i] = -1
            elif self.type.iloc[i] == "short":
                if pos <= self.takeprofit.iloc[i]:
                    perte = self.position.iloc[i] - self.takeprofit.iloc[i]
                    print("TP ", self.takeprofit.iloc[i], "gain =", perte)
                    info.makeTrade(perte)
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

io = Info(200)
st = Strategy()
da = Data()
da.getForexData("EURUSD=X", "1mo", "15m")
st.emaCrossing(da, io)
io.resume()

