import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
from strategy import Strategy
import pandas
class OneMinuteStrategy(Strategy.Strategy):

    def __init__(self, data):
        super().__init__(data)

    def test(self, affiche, debut, fin, levier=1, commission=0.01, capital=100):
        super().test(affiche, debut, fin, levier=levier, commission=commission, capital=capital)
        diff = 1
        self.addIndicator("ema_25")
        self.addIndicator("ema_50")
        self.addIndicator("ema_100")

# if self.data.iloc[line - interval, 5] > self.data.iloc[line - interval, 6] and ema_12 <= ema_36 and not cross and line > interval:
#                     cross = True

#                 if cross:
#                     if price < ema_12 and ema_36 < ema_12+(ema_12*(marge/100)) and not position:
#                         # short
#                         #print('short')
#                         nbDevise = capitalFin/float(price)
#                         #print('nbDevise', nbDevise)
#                         comm = nbDevise*commission
#                         totalCommission+=comm
#                         nbDevise = nbDevise - comm
#                         capTemp = capitalFin
#                         stopLoss = ema_36
#                         capitalFin = 0
#                         position = True
#                 if price >= stopLoss and position:
#                     #print('stop loss')
#                     cross = False
#                     gain = -((nbDevise*float(price))-capTemp)
#                     self.addGain(gain)
#                     capitalFin = nbDevise*float(price)
#                     #print("gain", gain)
#                     nbDevise = 0
#                     position = False
#                     pass
#                 if self.data.iloc[line - interval, 7] > 40 and adx <= 40 and stopLoss > 0 and position:
#                     # fin de short 
#                     #print("fin de position")
#                     stopLoss = -1
#                     gain = -((nbDevise*float(price))-capTemp)
#                     #print("gain", gain)
#                     self.addGain(gain)
#                     capitalFin = nbDevise*float(price)
#                     nbDevise = 0
#                     position = False
#                     cross = False

        
        

