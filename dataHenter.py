import pandas as pd


class DataHenter:
    def __init__(self, filsti) -> None:
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
        df = df.reset_index()
        df["år"] = df["år"].astype(int)
        return df
    