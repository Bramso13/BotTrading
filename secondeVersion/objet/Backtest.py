from Data import Data
from Info import Info
class BackTest:

    def __init__(self):
        self.data = Data()
        self.info = Info(200)

    def menu(self):
        fin = True
        while fin:
            choixData = 0
            print("Bienvenue dans le bot de trading !")
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
                debut = input("debut :")
                self.data.getBinanceData(devise=devise, timeframe=timeframe, debut=debut)
                fin = 0
            elif choixData == 2:
                print("Vous avez choisi des datas Forex.")
                devise = input("Veuillez entrer la devise souhaitée :")
                period = input("period :")
                interval = input("interval :")
                self.data.getForexData(devise, period, interval)
                fin = 0

back = BackTest()
back.menu()