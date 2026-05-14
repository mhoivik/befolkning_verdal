import pandas as pd

from dataHenter import DataHenter
from grafer import Grafer

class App:
    def __init__(self):
        self.stiUsorterData = r"ubehandlet_data.csv"
        self.df = None
        self.grafer = None 

    def Finnes(self, filnavn):
        try:
            open(filnavn).close()
            return True
        except:
            return False

    
    def Run(self):
        # sjekker at filen(e) er i orden
        if not self.Finnes("data.csv"):
            if not self.Finnes("ubehandlet_data.csv"):
                print("Error: Mangler inndata, kunne ikke kjøre programmet")
                raise FileNotFoundError("Verken ubehandlet_data.csv eller data.csv ble funnet")
            print("Behandler data...") 
            self.df = DataHenter(self.stiUsorterData).FormaterData()
            self.df.to_csv("data.csv")
        self.df = pd.read_csv('data.csv')
        

        graf = Grafer(self.df)
        # graf.DekadeStatisktikkTabell()
        graf.Befolkning()
        # graf.InnOgUtflytting()
        # graf.NettoFlytting()
        # graf.Folketilveksten()
        # graf.FodselsOverskudd()
        # graf.DekadeStatisktikkTabell()
        # graf.IllustrerStandardavvik("befolkning")
        