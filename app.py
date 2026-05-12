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
        if not self.Finnes("data.csv"):
            if not self.Finnes("ubehandlet_data.csv"):
                print("Error: Mangler inndata, kunne ikke kjøre programmet")
                return FileNotFoundError
            print("Behandler data...") 
            self.df = DataHenter(self.stiUsorterData).FormaterData()
            self.df.to_csv("data.csv")
        else:
            self.df = pd.read_csv('data.csv')
            print("Fant data.csv")
            print(self.df)
        

        grafer = Grafer(self.df)


            

