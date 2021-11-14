import ta
class Strategy:
    
    def __init__(self, data):
        self.data = data
        self.indicators = []
        self.winrate = 0
        self.nbTrade = 0
        self.nbPerte = 0
        self.nbGain = 0
        self.gain = 0
        self.maxGain = 0
        self.maxPerte = 0

    def setMaxGain(self, gain):
        if(gain > self.maxGain):
            self.maxGain = gain
    def getMaxGain(self):
        return self.maxGain
    
    def setMaxPerte(self, perte):
        if(perte < self.maxPerte):
            self.maxPerte = perte
    def getMaxPerte(self):
        return self.maxPerte

    def addGain(self, gain):
        self.nbTrade=+1
        if(gain < 0):
            self.nbPerte=+1
        elif gain > 0:
            self.nbGain=+1
        self.gain = self.gain + gain
    def getGain(self):
        return self.gain

    def setWinRate(self):
        self.winrate = (self.nbGain * 100)/self.nbTrade
    def getWinRate(self):
        return self.winrate

    def addIndicator(self, indicator):
        self.indicators.append(indicator)
        spli = indicator.split("_")
        if(spli[0] == "sma"):
            self.data["SMA"+spli[1].capitalize()] = ta.trend.sma_indicator(self.data['close'], int(spli[1]))
        if(spli[0] == "ema"):
            self.data["EMA"+spli[1].capitalize()] = ta.trend.ema_indicator(self.data['close'], int(spli[1]))
        if(spli[0] == "wma"):
            self.data["WMA"+spli[1].capitalize()] = ta.trend.wma_indicator(self.data['close'], int(spli[1]))
        if indicator == "macd":
            self.data["MACD"] = ta.trend.macd(self.data['close'])
        if indicator == "rsi":
            rsi = ta.momentum.RSIIndicator(self.data['close'])
            self.data["RSI"] = rsi.rsi()

    def afficheIndicators(self):
        i = 1
        print("Liste des indicateurs :")
        for indic in self.indicators:
            print(str(i)+" - "+str(indic))
            i=+1 

    


    