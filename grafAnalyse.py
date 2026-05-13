import numpy as np
from numpy.polynomial import Polynomial
import pandas as pd
import statsmodels.api as sm


class GrafAnalyse:
    def __init__(self, df):
        self.df = df
        return

    def FinnNullpunkt(self, polynom, definisjonsmengde=True):
        df = self.df
        roots = polynom.roots()
        reelleTall = roots[np.isreal(roots)].real
        innenDefinisjonsmengde = [i for i in reelleTall if df["år"].min() <= i <= df["år"].max()]
        return innenDefinisjonsmengde if definisjonsmengde else reelleTall
    
    def Regresjon(self, kolonneNavn, grad=4, punktListe=False):
        df = self.df
        x_akse = np.array(df["år"])
        y_akse = np.array(df[kolonneNavn])

        # flytter 1951 til null

        modell = Polynomial.fit(x_akse, y_akse, deg=grad)

        return modell(x_akse) if punktListe else modell

    def TangentDiskret(self, kolonneNavn, xValgt=1975):
        df = self.df
        if not xValgt in df["år"].values:
            return ValueError("x_koordinat tilhører ikke til definerte x-verdier")

        x = df["år"]
        x0 = xValgt
        y0 = df.loc[df["år"] == int(xValgt), kolonneNavn].item()
        yNeste = df.loc[df["år"] == int(xValgt)+1, kolonneNavn].item()
        yForrige = df.loc[df["år"] == int(xValgt)-1, kolonneNavn].item()

        a = (yNeste - yForrige) / 2
        b = a*x0 - y0 
        
        # Etpunktsformelen snudd
        linje = a * (x-x0) + y0
        return {
            "linje" : linje,
            'a' : a,
            'b' : b,
            'x' :x0,
            'y' :y0,
        }

    def GlidendeGjennomsnitt(self, kolonneNavn, k=7):
        return self.df[kolonneNavn].rolling(window=k).mean()
    
    def EksponensiellVektetGjennomsnitt(self, kolonneNavn, k=7):
        return self.df[kolonneNavn].ewm(span=k).mean()
    
    def LowessGlidendeRegresjon(self, kolonneNavn, frac=0.2):
        return sm.nonparametric.lowess(self.df[kolonneNavn], self.df["år"], frac=frac, return_sorted=False)