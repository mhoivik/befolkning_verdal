import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 


class DataHenter:
    def __init__(self, filsti):
        self.filsti = filsti
    
    def FormaterData(self):
        dfWide = pd.read_csv(self.filsti, sep=";", encoding="latin1", header=1)
        dfLong = dfWide.melt(id_vars=dfWide.columns[0], var_name="kolonne", value_name="verdi")

        dfLong[["år", "variabel"]] = dfLong["kolonne"].str.split(" ", n=1, expand=True)
        dfLong = dfLong.drop(columns=["region", "kolonne"])

        df = dfLong.pivot(index="år", columns="variabel",values="verdi").sort_index()
        df.rename(columns={
            "Befolkning 1. januar": "befolkning",
            "Levendefødte":         "fødte",
            "Døde":                 "døde",
            "Fødselsoverskudd":     "fødselsoverskudd",
            "Innflyttinger":        "innflytting",
            "Utflyttinger":         "utflytting",
            "Nettoinnflytting":     "netto_flytting",
            "Folketilvekst":        "folketilvekst",
        }, inplace=True)
        return df
    