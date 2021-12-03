import ta
from datetime import datetime
import pandas_ta as pda
class Strategy(object):
    
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
        self.gainP = 0
        self.totalCommission = 0

    def reinitialiser(self):
        self.data = "data"
        self.indicators = []
        self.winrate = 0
        self.nbTrade = 0
        self.nbPerte = 0
        self.nbGain = 0
        self.gain = 0
        self.maxGain = 0
        self.maxPerte = 0
        self.gainP = 0
        self.totalCommission = 0

    def setData(self, data):
        self.data = data

    def setTotalCommission(self, c):
        self.totalCommission = c
    def getTotalCommission(self):
        return self.totalCommission

    def setMaxGain(self, gain):
        if(gain > self.maxGain):
            self.maxGain = gain
    def getMaxGain(self):
        return self.maxGain

    def getGainP(self):
        return self.gainP
    def setGainP(self, gain):
        self.gainP = gain
    
    def setMaxPerte(self, perte):
        if(perte < self.maxPerte):
            self.maxPerte = perte
    def getMaxPerte(self):
        return self.maxPerte

    def addGain(self, gain):
        self.nbTrade+=1
        if gain < 0:

            self.setMaxPerte(gain)
            self.nbPerte+=1
        elif gain > 0:

            self.setMaxGain(gain)
            self.nbGain+=1
        self.gain = self.gain + gain
    def getGain(self):
        return self.gain

    def setWinRate(self):
        if(self.nbTrade > 0):
            self.winrate = (self.nbGain * 100)/self.nbTrade
    def getWinRate(self):
        return self.winrate

    def gainPourcent(self, base, gain):
        if(base > 0):
            self.setGainP(((gain*100)/base)-100)
            return ((gain*100)/base)-100

    def addIndicator(self, indicator, close):
        self.indicators.append(indicator)
        spli = indicator.split("_")
        if(spli[0] == "sma"):
            st = "SMA"+str(spli[1])
            self.data[st] = ta.trend.sma_indicator(close, int(spli[1]))
        if(spli[0] == "ema"):
            self.data["EMA"+spli[1].capitalize()] = ta.trend.ema_indicator(close, int(spli[1]))
        if(spli[0] == "wma"):
            self.data["WMA"+spli[1].capitalize()] = ta.trend.wma_indicator(close, int(spli[1]))
        if indicator == "macd":
            self.data["MACD"] = ta.trend.macd(close)
        if indicator == "rsi":
            rsi = ta.momentum.RSIIndicator(close)
            self.data["RSI"] = rsi.rsi()
        if indicator == "stoch_rsi":
            self.data["STOCH_RSI"] = ta.momentum.stochrsi(close)
        if indicator == "supertrend":
            ST_length = 20
            ST_multiplier = 3.0
            superTrend = pda.supertrend(self.data['High'], self.data['Low'], close, length=ST_length, multiplier=ST_multiplier)
            self.data['SUPER_TREND'] = superTrend['SUPERT_'+str(ST_length)+"_"+str(ST_multiplier)]
            self.data['SUPER_TREND_DIRECTION1'] = superTrend['SUPERTd_'+str(ST_length)+"_"+str(ST_multiplier)]

            ST_length = 20
            ST_multiplier = 4.0
            superTrend = pda.supertrend(self.data['High'], self.data['Low'], close, length=ST_length, multiplier=ST_multiplier)
            self.data['SUPER_TREND'] = superTrend['SUPERT_'+str(ST_length)+"_"+str(ST_multiplier)]
            self.data['SUPER_TREND_DIRECTION2'] = superTrend['SUPERTd_'+str(ST_length)+"_"+str(ST_multiplier)]

            ST_length = 40
            ST_multiplier = 8.0
            superTrend = pda.supertrend(self.data['High'], self.data['Low'], close, length=ST_length, multiplier=ST_multiplier)
            self.data['SUPER_TREND'] = superTrend['SUPERT_'+str(ST_length)+"_"+str(ST_multiplier)]
            self.data['SUPER_TREND_DIRECTION3'] = superTrend['SUPERTd_'+str(ST_length)+"_"+str(ST_multiplier)]
        if indicator == "adx":
            self.data["ADX"] = pda.adx(self.data['High'], self.data['Low'], close)["ADX_14"]
            

    def afficheIndicators(self):
        if(len(self.indicators) == 0):
            print("Pas d'indicateurs.")
        else:
            i = 1
            print("Liste des indicateurs :")
            for indic in self.indicators:
                print(str(i)+" - "+str(indic))
                i=+1 
    
    def test(self, affiche, debut, fin, levier=1, commission=0.01, capital = 100):
        if(affiche == 1):
            print("Lancement du backtest")
            print("Paramètres :")
            print("Capital = "+str(capital))
            print("Commission = "+str(commission))
            print("Levier = "+str(levier))
            print("Plage de date : de "+debut+" à ", fin)

    


    