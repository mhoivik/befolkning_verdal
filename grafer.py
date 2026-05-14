from grafAnalyse import GrafAnalyse

import numpy as np
from numpy.polynomial import Polynomial
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
        plt.rcParams.update(
            {
                "font.family": "DeJaVu Sans",
                "axes.titleweight": "bold",
                "axes.titlesize": 13,
            }
        )

        self.farge = {
            "bla": "#1a6fa8",
            "rod": "#c0392b",
            "lyseBla" : "#64b5f6",
            "lyseGronn": "#27ae60",
            "lyseRod" : "#F05D40",
            "oransje": "#e67e22",
            "lilla": "#8e44ad",
            "turkis": "#16a085",
            "morkBla": "#2c3e50",
            "gul": "#f1c40f",
            "rosa": "#e84393",
            "sand": "#d4a373",
            "morkRod": "#922b21",
            "lavendel": "#a29bfe",
            "cyan": "#00bcd4",
            "oliven": "#6b8e23",
            "kull": "#34495e",
            "gra": "#7f8c8d",
        }

    def Lagre(self):
        return

    def Befolkning(self):
        df = self.df

        plt.figure(figsize=(15, 5))
        plt.plot(df["år"], df["befolkning"], color=self.farge["bla"], label="Befolkning")
        plt.fill_between(df["år"], df["befolkning"], df.loc[df["år"].idxmin(), "befolkning"],
                          color=self.farge["lyseBla"], alpha=0.4)
        plt.annotate(f"Topp: {int(df["befolkning"].max()):,}".replace(',', ' '),
                    xy=(int(df["år"][df["befolkning"].idxmax()]), int(df["befolkning"].max())),
                    xycoords="data",
                    arrowprops=dict(arrowstyle="->", facecolor=self.farge["kull"], lw=1.2),
                    fontsize=8,
                    color=self.farge["kull"],
                    xytext=(-60, -40),
                    textcoords="offset points",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=self.farge["kull"], alpha=0.8)
                     )

        plt.annotate(f"Bunn: {int(df["befolkning"].min()):,}".replace(',', ' '),
                    xy=(int(df["år"][df["befolkning"].idxmin()]), int(df["befolkning"].min())),
                    xycoords="data",
                    arrowprops=dict(arrowstyle="->", facecolor=self.farge["kull"], lw=1.2),
                    fontsize=8,
                    color=self.farge["kull"],
                    xytext=(5, 20),
                    textcoords="offset points",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=self.farge["kull"], alpha=0.8)
                     )

        y_lim = plt.ylim()
        x_lim = plt.xlim()

        # Glidende gjennomsnitt mm
        """
        plt.plot(df["år"], self.analyse.GlidendeGjennomsnitt("befolkning"), color="black", label="Glidende Gjennomsnitt")
        plt.plot(df["år"], self.analyse.LowessGlidendeRegresjon("befolkning"), color="black", label="Lowess")
        plt.plot(df["år"], self.analyse.EksponensiellVektetGjennomsnitt("befolkning"), color="black", label="Lowess")
        """

        # Tangent
        """
        dataTangent = self.analyse.TangentDiskret("befolkning", 1974)
        plt.plot(df["år"], dataTangent["linje"], 
                 label=f"y = {dataTangent['a']}x {'+' if dataTangent['b'] > 0 else '-'} {abs(dataTangent['b'])}")
        plt.scatter(dataTangent['x'], dataTangent['y'], 
                    label=f"({np.int64(dataTangent['x'])}, {np.int64(dataTangent['y'])})", color=self.farge["kull"], zorder=5)
        """
        # Sekant
        """
        dataTangent = self.analyse.SekantDiskret("befolkning", 1970, 1980)
        plt.plot(df["år"], dataTangent["linje"], 
                 label=f"y = {dataTangent['a']:g}x {'+' if dataTangent['b'] > 0 else '-'} {abs(dataTangent['b']):g}")
        plt.scatter(dataTangent['x1'], dataTangent['y1'], 
                    label=f"({np.int64(dataTangent['x1'])}, {np.int64(dataTangent['y1'])})", color=self.farge["kull"], zorder=5)
        plt.scatter(dataTangent['x2'], dataTangent['y2'], 
                    label=f"({np.int64(dataTangent['x2'])}, {np.int64(dataTangent['y2'])})", color=self.farge["kull"], zorder=5)
        """

        
        # Regresjon 
        """
        plt.plot(df["år"], self.analyse.Regresjon("befolkning", 36, True), 
                 color=self.farge["rod"], label="Regresjon")
        """

        # Første- og andrederivert || Finn nullpunkt
        """
        regresjon = self.analyse.Regresjon("befolkning", 36)
        forsteDerivert = regresjon.deriv() 
        andreDerivert = regresjon.deriv(m=2)
        plt.plot(df["år"], forsteDerivert(df["år"]), label="Førstederivert", color=self.farge["lavendel"])
        plt.plot(df["år"], andreDerivert(df["år"]), label="Andrederivert", color=self.farge["rosa"])

        print(list(map(float, self.analyse.FinnNullpunkt(regresjon))))
        print(list(map(float, self.analyse.FinnNullpunkt(forsteDerivert))))
        print(list(map(float, self.analyse.FinnNullpunkt(andreDerivert))))
        """

        # Aker etb
        """
        plt.axvline(x=1971.0, color=self.farge["kull"], 
                    label="Verftet åpnet (1969)", linestyle=":")
        plt.annotate("Etablering av verft (1969)", (1972, 910), color=self.farge["kull"])
        """

        plt.title("Befolkning Verdal Kommune 1951-2025")
        plt.xlabel("År")
        plt.ylabel("Befolkning")

        plt.xlim(x_lim)
        plt.ylim(y_lim)

        plt.legend(frameon=False)
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

        plt.figure(figsize=(16,9))
        plt.plot(df["år"], df["innflytting"], color=self.farge["lyseGronn"], label="Innflytting")
        plt.plot(df["år"], df["utflytting"], color=self.farge["lyseRod"], label="Utflytting")


        # lowess
        """
        plt.plot(
            df["år"],
            self.analyse.LowessGlidendeRegresjon("innflytting"),
            color=self.farge["oliven"],
            label="Lowess regresjon - Innflytting",
            alpha=0.7,
            linestyle=":"
        )
        plt.plot(
            df["år"],
            self.analyse.LowessGlidendeRegresjon("utflytting"),
            color=self.farge["morkRod"],
            label="Lowess regresjon - Utfytting",
            alpha=0.7,
            linestyle=":"
        )
        """

        # Aker etb
        """
        plt.axvline(x=1971.0, color=self.farge["kull"], 
                    label="Verftet åpnet (1969)", linestyle="--")
        plt.annotate("Etablering av verft (1969)", (1972, 910), color=self.farge["kull"])
        """

        plt.title("Inn- og utflytting Verdal Kommune 1951-2025")
        plt.xlabel("År")
        plt.ylabel("Antall")

        # plt.ylim()
        # plt.xlim(1951, 2025)

        plt.legend(frameon=False)
        plt.show()
        return

    def NettoFlytting(self):
        df = self.df
        
        plt.figure(figsize=(16,9))

        plt.plot(df["år"], df["netto_flytting"],
                color=self.farge["sand"],
                label="Netto flytting"
                )
        plt.axhline(y=0, linestyle="--", color=self.farge["kull"], alpha=0.6)
        plt.fill_between(df["år"], df["netto_flytting"], 0, where=(df["netto_flytting"] > 0),
                         color=self.farge["lyseGronn"],
                         alpha=0.4,
                         interpolate=True
                         )
        plt.fill_between(df["år"], df["netto_flytting"], 0, where=(df["netto_flytting"] < 0),
                         color=self.farge["lyseRod"],
                         alpha=0.4,
                         interpolate=True
                         )

        plt.plot(
            df["år"],
            self.analyse.LowessGlidendeRegresjon("netto_flytting"),
            color=self.farge["oliven"],
            label="Lowess frac=0.2",
            alpha=0.7,
            linestyle=":"
        )

        plt.title("Netto flytting Verdal Kommune 1951 - 2025")
        plt.xlabel("År")
        plt.ylabel("Antall")

        plt.legend(frameon=False)
        plt.show()

    def StatistikkTabell(self):
        df = self.df
        return
    
    def DekadeStatisktikkTabell(self):
        df = self.df

        df["fødsels_prosent"] = df["fødte"] / df["befolkning"] * 100
        df["døde_prosent"] = df["døde"] / df["befolkning"] * 100
        df["flytte_prosent"] = df["netto_flytting"] / df["befolkning"] * 100

        df["dekade"] = (df["år"] // 10) * 10
        gruppe = df.groupby("dekade", as_index=False)[
            ["fødsels_prosent", "døde_prosent", "flytte_prosent"]].mean()

        avrundetGruppe = gruppe.round(2)
        header = ["Tiår", "Andel føde", "Andel døde", "Andel flyttet"]
                
        return

    def KjorAlle(self):
        return

