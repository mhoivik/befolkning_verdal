import numpy as np
import pandas as pd
import statsmodels.api as sm


class GrafAnalyse:
    def __init__(self, df):
        self.df = df
        return

    def GlidendeGjennomsnitt(self, kolonneNavn, k=7):
        return self.df[kolonneNavn].rolling(window=k).mean()
    
    def EksponensiellVektetGjennomsnitt(self, kolonneNavn, k=7):
        return self.df[kolonneNavn].ewm(span=k).mean()
    
    def LowessGlidendeRegresjon(self, y_akse, frac=0.2):
        return sm.nonparametric.lowess(self.df[y_akse], self.df["år"], frac=frac, return_sorted=False)