from Data import Data
from Info import Info
from Strategy import Strategy
class BackTest:

    def __init__(self):
        self.data = Data()
        self.info = Info(200)

    def menu(self):
        fin = True
        strategies = Strategy.strategies
        choixStrat = -1
        while fin:
            choixData = 0
            print("Bienvenue dans le bot de trading !")
            cap = float(input("Insérer votre capital :"))
            if cap < 0:
                raise Exception("Le capital entré est négatif")
            self.info.setCapital(cap)
            self.info.fin = cap
            levier = float(input("Insérez le levier souhaitée :"))
            if levier < 1:
                raise Exception("Le levier saisi est incorrect")
            self.info.levier = levier
            print("Veuillez choisir une source de data :")
            print("1 - Binance")
            print("2 - Forex")
            choixData = input("Entrez votre choix :")
            choixData = int(choixData)
            if (choixData != 1 or choixData != 2):
                print("Veuillez entrer un chiffre (1 ou 2)")
                pass
            if choixData == 1:
                print("Vous avez choisi des datas Binance.")
                devise = input("Veuillez entrer la devise souhaitée :")
                timeframe = input("timeframe :")
                jour = input("jour :")
                mois = input("mois :")
                année = input("année :")
                debut = jour + " " + mois + " " + année
                self.data.getBinanceData(devise=devise, timeframe=timeframe, debut=debut)
            elif choixData == 2:
                print("Vous avez choisi des datas Forex.")
                devise = input("Veuillez entrer la devise souhaitée :")
                period = input("period :")
                interval = input('interval :')
                self.data.getForexData(devise, period, interval)
            print("Veuillez choisir une stratégie à tester :")
            i = 1
            for s in strategies:
                print(i, "-", s)
                i += 1
            choixStrat = int(input("Votre choix ?"))
            if choixStrat <= len(strategies) and choixStrat >= 1:
                print("Vous avez choisi : ", strategies[choixStrat - 1])
                m = globals()['Strategy']()
                func = getattr(m, strategies[choixStrat - 1])
                func(self.data, self.info)
                self.info.resume()
                fin = False
            else:
                raise Exception('Veuillez choisir un chiffre valide')


back = BackTest()
back.menu()