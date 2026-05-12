import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os


class Grafer:
    def __init__(self, df, outputMappe="grafer"):
        self.df = df
        self.sti = outputMappe
        os.makedirs(self.sti, exist_ok=True)

    def Befolkning(self):
        df = self.df
        plt.plot(df["år"], df["befolkning"])
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