
class Info:

    def __init__(self, capital, levier=1):
        self.capital = capital
        self.levier = levier
        self.nbTrade = 0
        self.nbTradeG = 0
        self.nbTradeP = 0
        self.gainMax = 0
        self.perteMax = 0
        self.fin = capital

    def setCapital(self, capital):
        self.capital = capital

    def makeTrade(self, gain : float):
        self.nbTrade+=1
        self.fin = self.fin+gain
        if gain > 0:
            self.nbTradeG+=1
            self.gainMax = gain if gain > self.gainMax else self.gainMax
        else:
            self.nbTradeP+=1
            self.perteMax = gain if gain < self.perteMax else self.perteMax

    def getWinrate(self) -> float:
        if self.nbTrade != 0 and self.nbTradeG != 0:
            return (self.nbTradeG / self.nbTrade) * 100
        return 0

    def getBenefice(self):
        return self.fin - self.capital

    def getBeneficePourcent(self):
        return ((self.getBenefice() / self.capital) * 100)

    def getFinCap(self):
        return self.fin

    def resume(self):
        print("Résumé :")
        print("Winrate =", self.getWinrate(), "%")
        print("Capital de départ :", self.capital)
        print("Capital de fin :", self.getFinCap())
        print("Bénéfice :", self.getBenefice())
        print("Benefice en % :", self.getBeneficePourcent())
        print("Nombre de trade gagnant :", self.nbTradeG)
        print("Nombre de trade perdant :", self.nbTradeP)
        print("Max perte :", self.perteMax, (self.perteMax / self.capital)*100, "%")
        print("Max gain :", self.gainMax, (self.gainMax / self.capital)*100, "%")