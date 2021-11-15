import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
from strategy import Strategy
import pandas
class OneMinuteStrategy(Strategy.Strategy):

    def __init__(self, data):
        super().__init__(data)

    def test(self, debut, fin, levier=1, commission=0.01, capital=100):
        super().test(debut, fin, levier=levier, commission=commission, capital=capital)
        diff = 1
        self.addIndicator("ema_25")
        self.addIndicator("ema_50")
        self.addIndicator("ema_100")

        for d in self.data:
            if(d["close"] > )
        

