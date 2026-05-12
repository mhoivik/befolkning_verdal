from grafAnalyse import GrafAnalyse

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os



class Grafer:
    def __init__(self, df, outputMappe="grafer"):
        self.df = df
        self.analyse = GrafAnalyse(df)

        self.StandardStil()

        self.sti = outputMappe
        os.makedirs(self.sti, exist_ok=True)
    
    def StandardStil(self):
        plt.style.use("ggplot")
        plt.rcParams.update({
            "font.family" : "DeJaVu Sans",
            "axes.titleweight" : "bold",
            "axes.titlesize" : 13
        })


    def Lagre(self):
        return


    def Befolkning(self):
        df = self.df
 
        plt.figure(figsize=(15,5))
        plt.plot(df["år"], df["befolkning"], color="red", label="Befolkning")
        # plt.plot(df["år"], self.analyse.LowessGlidendeRegresjon("befolkning"), color="black", label="Glidende Gjennomsnitt")
        plt.title("Befolkning Verdal Kommune 1951-2025")
        plt.xlabel("År")
        plt.ylabel("Befolkning")

        # plt.ylim()
        plt.xlim(1951, 2025) 

        plt.legend()
        plt.show()
        return
   
    def BefolkningsVekst(self):
        df = self.df
        return

    def LevendefodtMotDode(self):
        df = self.df
        return

    def InnOgUtflytting(self):
        df = self.df
        return
    
    def StatistikkTabell(self):
        df = self.df
        return
    
    def KjorAlle(self):
        return 