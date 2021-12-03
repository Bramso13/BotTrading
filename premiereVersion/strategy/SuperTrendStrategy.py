from strategy import Strategy
class SuperTrendStrategy(Strategy.Strategy):

    def __init__(self, data) -> None:
        super().__init__(data)
        
    def test(self, affiche, debut, fin, levier=1, commission=0.01, capital = 100):
        try:
            super().test(affiche, debut, fin, levier, commission, capital)
            
            self.addIndicator('rsi', self.data["Close"]) # 4
            self.addIndicator('ema_90', self.data["Close"]) #5 
            self.addIndicator('stoch_rsi', self.data["Close"]) #6
            self.addIndicator('supertrend', self.data["Close"]) #7
            #print(self.data)

            capitalFin = capital
            totalCommission = 0
            nbDevise = 0
            d=0
            for d in range(0,len(self.data)-1):
                if capitalFin > 0 and self.data.iloc[d, 9]+self.data.iloc[d, 10]+self.data.iloc[d, 11] >= 1 and self.data.iloc[d, 3] > self.data.iloc[d, 6] and self.data.iloc[d, 7] < 0.8:
                    #print("buy")
                    
                    nbDevise = capitalFin/float(self.data.iloc[d, 3])
                    comm = nbDevise*commission
                    totalCommission+=comm
                    nbDevise = nbDevise - comm
                    capTemp = capitalFin
                    capitalFin = 0
                elif nbDevise > 0 and self.data.iloc[d, 9]+self.data.iloc[d, 10]+self.data.iloc[d, 11] < 1 and self.data.iloc[d, 7] > 0.2:
                    #print("sell")
                    gain = (nbDevise*float(self.data.iloc[d, 3]))-capTemp
                    #print("gain", gain)
                    self.addGain(gain)
                    capitalFin = nbDevise*float(self.data.iloc[d, 3])
                    nbDevise = 0
                else:
                    continue
                    #print('pas d"oportunité.')
            self.setWinRate()
            self.setTotalCommission(totalCommission)
            winrate = self.getWinRate()
            if capitalFin == 0:
                gainP = self.gainPourcent(capital, capTemp)
            else:
                gainP = self.gainPourcent(capital, capitalFin)
            if(affiche == 1):
                print("capitalFin = ", str(capitalFin), self.nbPerte, self.nbGain)
                print("winrate = ", str(winrate))
                print("plus value % =", str(gainP))
        except Exception as err:
            print(format(err))


        return self.data
            

