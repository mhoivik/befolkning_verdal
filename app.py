import pandas as pd

from logger import Logg
from dataHenter import DataHenter
from grafer import Grafer


"""Hovedklassen, har ansvar for de større underobjektene og kjøring av programmet"""


class App:
    def __init__(self) -> None:
        Logg(self, "Starter...")
        self.stiUsorterData = r"ubehandlet_data.csv"
        self.stiData = r"data.csv"
        self.df = None

    def __del__(self) -> None:
        Logg(self, "Alle oppgaver fullført")
        Logg(self, "Deinitialisert...")

    def Finnes(self, filnavn):
        Logg(self, f"Sjekker om {filnavn} finnes...")
        try:
            open(filnavn).close()
            return True
        except:
            return False

    
    def Run(self) -> None:
        # sjekker at filen(e) er i orden
        if not self.Finnes(self.stiData):
            if not self.Finnes(self.stiUsorterData):
                print("Error: Mangler inndata, kunne ikke kjøre programmet")
                raise FileNotFoundError("Verken ubehandlet_data.csv eller data.csv ble funnet")
            Logg(self, "Har ikke data.csv")
            Logg(self, "Behandler data...")
            self.df = DataHenter(self.stiUsorterData).FormaterData()
            self.df.to_csv(self.stiData, index=False)
            Logg(self, "Data behandlet")


        self.df = pd.read_csv(self.stiData)
        """ Profesjonell index reseting"""

        Logg(self, "Fil godkjent")
        Logg(self, "Begynner med grafer")
        

        graf = Grafer(self.df)
        graf.TegnAlleGrafer()

        """Har Implementering"""
        # graf.DekadeStatisktikkTabell()
        # graf.Befolkning()
        # graf.InnOgUtflytting()
        # graf.NettoFlytting()
        # graf.Folketilveksten()
        # graf.FodselsOverskudd()

        """Ikke Implementer"""
        # graf.IllustrerStandardavvik("befolkning")


        