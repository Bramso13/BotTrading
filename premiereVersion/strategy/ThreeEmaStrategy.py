from strategy import Strategy

class ThreeEmaStrategy(Strategy.Strategy):

    def __init__(self, data):
        super().__init__(data)

    def test(self, affiche, debut, fin, levier=1, commission=0.01, capital = 100):
        super().test(affiche, debut, fin, levier=1, commission=0.01, capital = 100)
        
        try:
            self.addIndicator('ema_25', self.data["Close"]) #5
            self.addIndicator('ema_50', self.data["Close"]) #6
            self.addIndicator('ema_100', self.data["Close"]) #7

            marge = 1
            multi = 1.5
            detectTrend = False
            detectRebond = False
            takeProfit = -1
            stopLoss = -1
            capitalFin = capital
            totalCommission = 0
            nbDevise = 0
            position = False
            
            for line in range(0, len(self.data)):
                ema_100 = self.data.iloc[line, 7]
                ema_50 = self.data.iloc[line, 6]
                ema_25 = self.data.iloc[line, 5]
                price = self.data.iloc[line, 3]
                priceC = price > ema_25+(price*(marge/100))
                priceV = ema_25 > ema_50+(ema_25*(marge/100))
                priceCIN = ema_50 > ema_100+(ema_50*(marge/100))
                if (priceC and priceV and priceCIN and not detectTrend):
                    detectTrend = True
                if detectTrend and not detectRebond:
                    if price <= ema_50-(price*(marge/100)):
                        detectRebond = True
                if detectRebond:
                    if price < ema_100:
                        detectTrend = False
                        detectRebond = False
                        position = False
                        pass
                    if price >= ema_25 and not position:
                        # buy
                        #print("buy")
                        stopLoss = ema_50
                        takeProfit = price + (price - stopLoss)*multi
                        nbDevise = capitalFin/float(price)
                        comm = nbDevise*commission
                        totalCommission+=comm
                        nbDevise = nbDevise - comm
                        capTemp = capitalFin
                        capitalFin = 0
                        position = True
                if takeProfit > 0 and stopLoss > 0:
                    if price >= takeProfit or price <= stopLoss:
                        #sell
                        #print("sell")
                        stopLoss = -1
                        takeProfit = -1 
                        gain = (nbDevise*float(price))-capTemp
                        self.addGain(gain)
                        capitalFin = nbDevise*float(price)
                        nbDevise = 0
                        detectTrend = False
                        detectRebond = False
                        position = False
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

