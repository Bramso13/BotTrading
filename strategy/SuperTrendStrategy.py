from Strategy import Strategy
class SuperTrendStrategy(Strategy):

    def __init__(self, data) -> None:
        super().__init__(data)
        
    def test(self, debut, fin, levier=1, commission=0.01, capital = 100):
        super().test(debut, fin, levier, commission, capital)


s = SuperTrendStrategy("data")
s.afficheIndicators()