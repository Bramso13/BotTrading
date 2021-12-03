from numpy import positive
from strategy import Strategy

class RideTheTrendStrategy(Strategy.Strategy):

    def __init__(self, data):
        super().__init__(data)

    def test(self, affiche, debut, fin, levier=1, commission=0.01, capital = 100):
        super().test(affiche, debut, fin, levier=1, commission=0.01, capital = 100)
        
        try:
            # indicators
            self.addIndicator("ema_12", self.data['Close'])#5
            self.addIndicator("ema_36", self.data['Close'])#6
            self.addIndicator("adx", self.data["Close"])
            #print(self.data)
            marge = 0.5
            interval = 3
            cross = False
            position = False
            stopLoss = -1
            capitalFin = capital
            totalCommission = 0
            nbDevise = 0
            capTemp = capital
            for line in range(0,len(self.data)):
                ema_12 = self.data.iloc[line, 5] # blue
                ema_36 = self.data.iloc[line, 6]
                adx = self.data.iloc[line, 7]
                price = self.data.iloc[line, 3]

                if line > interval and self.data.iloc[line - interval, 5] < self.data.iloc[line - interval, 6] and ema_12 >= ema_36:
                    cross = True
                if cross:

                    if price > ema_12 and ema_12 > ema_36+(0.003) and not position:
                        # long position
                        nbDevise = capitalFin/float(price)
                        #print('nbDevise', nbDevise)
                        comm = nbDevise*commission
                        totalCommission+=comm
                        nbDevise = nbDevise - comm
                        capTemp = capitalFin
                        stopLoss = ema_36
                        capitalFin = 0
                        position = True
                if price <= stopLoss and position:
                    #print('stop loss')
                    cross = False
                    gain = (nbDevise*float(price))-capTemp
                    self.addGain(gain)
                    capitalFin = nbDevise*float(price)
                    #print("gain", gain)
                    nbDevise = 0
                    position = False
                    pass
                if self.data.iloc[line - interval, 7] > 40 and adx <= 40 and stopLoss > 0 and position:
                    # fin de long  
                    #print("fin de position")
                    stopLoss = -1
                    gain = (nbDevise*float(price))-capTemp
                    #print("gain", gain)
                    self.addGain(gain)
                    capitalFin = nbDevise*float(price)
                    nbDevise = 0
                    position = False
                    cross = False



            #print('capitalfin', capitalFin)
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


