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
        y_lim = plt.ylim()
        x_lim = plt.xlim()

        # Glidende gjennomsnitt mm
        """
        plt.plot(df["år"], self.analyse.LowessGlidendeRegresjon("befolkning"), color="black", label="Glidende Gjennomsnitt")
        """

        # Tangent
        """
        dataTangent = self.analyse.TangentDiskret("befolkning", 1974)
        plt.plot(df["år"], dataTangent["linje"], 
                 label=f"{dataTangent['a']}x {'+' if dataTangent['b'] > 0 else '-'} {abs(dataTangent['b'])}")
        plt.scatter(dataTangent['x'], dataTangent['y'], 
                    label=f"({dataTangent['x']}, {dataTangent['y']})", color=self.farge["kull"], zorder=5)
        """

        # Regresjon 
        """
        plt.plot(df["år"], self.analyse.Regresjon("befolkning", 36, True), 
                 color=self.farge["rod"], label="Regresjon")
        """

        # Første- og andrederivert
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

        plt.figure()
        plt.plot(df["år"], df["innflytting"], color="green", label="Innflytting")
        plt.plot(df["år"], df["utflytting"], color="red", label="Utflytting")
        plt.plot(
            df["år"],
            self.analyse.LowessGlidendeRegresjon("innflytting"),
            color="black",
            label="Lowess regresjon - Innflytting",
        )
        plt.plot(
            df["år"],
            self.analyse.LowessGlidendeRegresjon("utflytting"),
            color="gray",
            label="Lowess regresjon - Utfytting",
        )

        plt.title("Inn- og utflytting Verdal Kommune 1951-2025")
        plt.xlabel("År")
        plt.ylabel("Antall")

        # plt.ylim()
        # plt.xlim(1951, 2025)

        plt.legend(frameon=False)
        plt.show()
        return

    def StatistikkTabell(self):
        df = self.df
        return

    def KjorAlle(self):
        return

