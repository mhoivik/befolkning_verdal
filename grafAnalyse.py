import numpy as np
from numpy.polynomial import Polynomial
import pandas as pd
import statsmodels.api as sm


class GrafAnalyse:
    """ Implementering av metoder for analyse av data.
        Mesteparten er hentet fra 7D, men og litt fra resten av R1 boka """
    def __init__(self, df):
        self.df = df
        return

    def LeggInnKolonne(self, kolonneNavn, kolonne):
        self.df[kolonneNavn] = kolonne


    def FinnNullpunkt(self, polynom, definisjonsmengde=True):
        df = self.df.copy()     # .copy() fordi at df egenlig er en ptr. Bedre prakis
        roots = polynom.roots()
        reelleTall = roots[np.isreal(roots)].real
        innenDefinisjonsmengde = [i for i in reelleTall if df["år"].min() <= i <= df["år"].max()]
        return innenDefinisjonsmengde if definisjonsmengde else reelleTall
    

    def Regresjon(self, kolonneNavn, grad=4, punktListe=False):
        df = self.df.copy()
        x_akse = np.array(df["år"])
        y_akse = np.array(df[kolonneNavn])

        modell = Polynomial.fit(x_akse, y_akse, deg=grad)

        return modell(x_akse) if punktListe else modell


    def TangentDiskret(self, kolonneNavn, x0=1975):
        df = self.df.copy()
        if not int(x0) in df["år"].values:
            raise ValueError("x_koordinat tilhører ikke til definerte x-verdier")

        x = df["år"]
        y0 = df.loc[df["år"] == int(x0), kolonneNavn].values[0]
        yNeste = df.loc[df["år"] == int(x0)+1, kolonneNavn].values[0]
        yForrige = df.loc[df["år"] == int(x0)-1, kolonneNavn].values[0]

        a = (yNeste - yForrige) / 2
        b = y0 - a*x0
        
        # Etpunktsformelen snudd
        linje = a * (x-x0) + y0
        return {
            "linje" : linje,
            'a' : a,
            'b' : b,
            'x' :x0,
            'y' :y0,
        }
    
    def SekantDiskret(self, kolonneNavn, x1=1970, x2=1980):
        df = self.df.copy()

        if not int(x1) in df["år"].values:
            raise ValueError("x_koordinat tilhører ikke til definerte x-verdier")
        if not int(x2) in df["år"].values:
            raise ValueError("x_koordinat tilhører ikke til definerte x-verdier")

        x = df["år"]
        y1 = df.loc[df["år"] == int(x1), kolonneNavn].values[0]
        y2 = df.loc[df["år"] == int(x2), kolonneNavn].values[0]

        a = (y2 - y1) / (x2 -x1)
        b = y1 -a*x1


        linje = a * (x-x1) + y1

        return {
            "linje" : linje,
            'a' : a,
            'b' : b,
            "x1" :x1,
            "y1" :y1,
            "x2" :x2,
            "y2" :y2
        }


    def GlidendeGjennomsnitt(self, kolonneNavn, k=7):
        return self.df[kolonneNavn].rolling(window=k).mean()

    def EksponensiellVektetGjennomsnitt(self, kolonneNavn, k=7):
        return self.df[kolonneNavn].ewm(span=k).mean()

    
    def LowessGlidendeRegresjon(self, kolonneNavn, frac=0.2):
        return sm.nonparametric.lowess(self.df[kolonneNavn], self.df["år"], frac=frac, return_sorted=False)