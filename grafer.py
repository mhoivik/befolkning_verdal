import os
import inspect

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from logger import Logg
import konfig
from grafAnalyse import GrafAnalyse


# ToDo
# - Forklaring og kommentarer


"""
Kommentarer, prinsipp og ekstrainformasjon, tankegang finnes i Grafer::Befolkning(). 
Resten av funksjonene ligner veldig og er ikke like bra dokumentert

"""

class Grafer:
    """Tegner (og lagrer) grafer"""
    def __init__(self, df: pd.DataFrame, outputMappe: str="grafer") -> None:
        self.df = df.copy() # .copy() for å lag en kopi og ikke bare bruke ptr til objektet. (bedre sikkerhet)
        self.analyse = GrafAnalyse(df)

        # design til grafene
        self.__StandardStil()

        self.mappe = outputMappe
        os.makedirs(self.mappe, exist_ok=True)
        Logg(self, "Konstruktør variabler OK")

# PRIVATE:

    def __Ferdigstill(self, filNavn: str = None) -> None:
        if filNavn is None: filNavn = f"{inspect.stack()[1].function.lower()}.png"
        if konfig.SKRIV_TIL_PNG:
            sti = os.path.join(self.mappe, filNavn)
            plt.savefig(sti, dpi=150, bbox_inches="tight", facecolor="white")
            plt.close()
        else:
            plt.show()
        Logg(self, f"{inspect.stack()[1].function} er ferdig")


    def __StandardStil(self) -> None:
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
            "lyseBla": "#64b5f6",
            "lyseGronn": "#27ae60",
            "lyseRod": "#F05D40",
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
            "blaHvit": "#eaf2fb"
        }



# PUBLIC:

    def Befolkning(self) -> None:   # -> None viser at funksjonen ikke returner noe (void). Øker typesikkerhet
        df = self.df

        plt.figure(figsize=(16, 9)) # Dimmensjon på vinduet
        plt.plot(                   # selve grafen
            df["år"], df["befolkning"], color=self.farge["bla"], label="Befolkning"
        )
        plt.fill_between(           # fyllmassen under grafen
            df["år"],
            df["befolkning"],
            df.loc[df["år"].idxmin(), "befolkning"],
            color=self.farge["lyseBla"],
            alpha=0.4,
        )

        plt.annotate(               # Tekst med info om ekstremalpunktet, med pil og tekstboks
            f"Topp: {int(df['befolkning'].max()):,}".replace(",", " "),
            xy=(int(df["år"][df["befolkning"].idxmax()]), int(df["befolkning"].max())),
            xycoords="data",
            arrowprops=dict(arrowstyle="->", facecolor=self.farge["kull"], lw=1.2),
            fontsize=8,
            color=self.farge["kull"],
            xytext=(-60, -40),
            textcoords="offset points",
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor="white",
                edgecolor=self.farge["kull"],
                alpha=0.8,
            ),
        )

        plt.annotate(                # --""--
            f"Bunn: {int(df['befolkning'].min()):,}".replace(",", " "),
            xy=(int(df["år"][df["befolkning"].idxmin()]), int(df["befolkning"].min())),
            xycoords="data",
            arrowprops=dict(arrowstyle="->", facecolor=self.farge["kull"], lw=1.2),
            fontsize=8,
            color=self.farge["kull"],
            xytext=(5, 20),
            textcoords="offset points",
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor="white",
                edgecolor=self.farge["kull"],
                alpha=0.8,
            ),
        )

        # Lagrer bestemelsen av grensene av aksene, før andre grafer kan påvirke
        y_lim = plt.ylim()
        x_lim = plt.xlim()
        
        
        # Aker est linje
        """"""
        plt.axvline(x=1969.0, color=self.farge["kull"], 
                    label="Verftet åpnet (1969)", linestyle=":")
        plt.annotate("Etablering av verft (1969)", (1971, 910), color=self.farge["kull"])
        """"""




        # EKSEMPLER FOR DATAANALYSE-VERKTØY:

        # Glidende gjennomsnitt mm
        """
        plt.plot(df["år"], self.analyse.GlidendeGjennomsnitt("befolkning"), color="black", label="Glidende Gjennomsnitt")
        plt.plot(df["år"], self.analyse.LowessGlidendeRegresjon("befolkning"), color="red", label="Lowess")
        plt.plot(df["år"], self.analyse.EksponensiellVektetGjennomsnitt("befolkning"), color="green", label="EWM Gjennomsnitt")
        """

        # Tangent
        """
        dataSekant = self.analyse.TangentDiskret("befolkning", 1974)
        plt.plot(df["år"], dataSekant["linje"], 
                 label=f"y = {dataSekant['a']}x {'+' if dataSekant['b'] > 0 else '-'} {abs(dataSekant['b'])}")
        plt.scatter(dataSekant['x'], dataSekant['y'], 
                    label=f"({np.int64(dataSekant['x'])}, {np.int64(dataSekant['y'])})", color=self.farge["kull"], zorder=5)
        """

        # Sekant
        """"""
        dataSekant = self.analyse.SekantDiskret("befolkning", 1969, 1980)
        plt.plot(df["år"], dataSekant["linje"], 
                 label=f"y = {dataSekant['a']:g}x {'+' if dataSekant['b'] > 0 else '-'} {abs(dataSekant['b']):g}")
        plt.scatter(dataSekant['x1'], dataSekant['y1'], 
                    label=f"({np.int64(dataSekant['x1'])}, {np.int64(dataSekant['y1'])})", color=self.farge["kull"], zorder=5)
        plt.scatter(dataSekant['x2'], dataSekant['y2'], 
                    label=f"({np.int64(dataSekant['x2'])}, {np.int64(dataSekant['y2'])})", color=self.farge["kull"], zorder=5)
        """"""

        # Projekter bane for folkevekst verdal
        """
        dataSekant = self.analyse.SekantDiskret("befolkning", 1951, 1969)
        plt.plot(df["år"], dataSekant["linje"], 
                 label=f"y = {dataSekant['a']:g}x {'+' if dataSekant['b'] > 0 else '-'} {abs(dataSekant['b']):g}",
                   color="blue", linestyle="--")
        plt.scatter(dataSekant['x1'], dataSekant['y1'], 
                    label=f"({np.int64(dataSekant['x1'])}, {np.int64(dataSekant['y1'])})", color=self.farge["kull"], zorder=5)
        plt.scatter(dataSekant['x2'], dataSekant['y2'], 
                    label=f"({np.int64(dataSekant['x2'])}, {np.int64(dataSekant['y2'])})", color=self.farge["kull"], zorder=5)
        plt.fill_between(           # fyllmassen under grafen
            df["år"],
            df["befolkning"],
            dataSekant["linje"],
            where=df["befolkning"] > dataSekant["linje"],
            color=self.farge["lyseGronn"],
            alpha=0.4,
        )
        """




        # Regresjon (ligner litt på en Taylor serie)
        """
        plt.plot(df["år"], self.analyse.Regresjon("befolkning", 5, True), 
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

        # Aksetitler
        plt.title("Befolkning Verdal Kommune 1951-2025")
        plt.xlabel("År")
        plt.ylabel("Befolkning")

        # Setter grafene til de definerte målene
        plt.xlim(x_lim)
        plt.ylim(y_lim)

        plt.legend(
                frameon=False,
                loc="upper left"
                   )                # Tekstboksen i hjørne med info om alle grafene inkl
        self.__Ferdigstill()        # Lagrer grafen som png eller viser den i et vindu


    def BefolkningsVekst(self) -> None:
        """IKKE IMPL"""
        df = self.df
        # self.__Ferdigstill()


    def LevendefodtMotDode(self) -> None:
        df = self.df
        plt.figure()
        plt.plot(df["år"], df["fødte"], color="red", label="Levendefodte")
        plt.plot (df["år"], df["døde"],color="blue", label="Døde")
        plt.title("Levendefodte_vs_døde - verdal 1951-2025")
        plt.xlabel("År")
        plt.ylabel("Antall")
        plt.legend(frameon=False, loc="upper left")
        self.__Ferdigstill() # plt.savefig(path)


    def Folketilveksten(self) -> None:
        df = self.df

        plt.figure(figsize=(16, 9))

        plt.plot(
            df["år"],
            df["folketilvekst"],
            color=self.farge["lilla"],
            label="Folketilvekst",
        )
        plt.axhline(y=0, linestyle="--", color=self.farge["kull"], alpha=0.6)
        plt.fill_between(
            df["år"],
            df["folketilvekst"],
            0,
            where=(df["folketilvekst"] > 0),
            color=self.farge["lyseGronn"],
            alpha=0.4,
            interpolate=True,
        )
        plt.fill_between(
            df["år"],
            df["folketilvekst"],
            0,
            where=(df["folketilvekst"] < 0),
            color=self.farge["lyseRod"],
            alpha=0.4,
            interpolate=True,
        )

        plt.plot(
            df["år"],
            self.analyse.EksponensiellVektetGjennomsnitt("folketilvekst"),
            color=self.farge["turkis"],
            label="EWM algoritme",
            alpha=0.7,
            linestyle=":",
        )

        plt.title("Total folketilvekst Verdal Kommune 1951 - 2025")
        plt.xlabel("År")
        plt.ylabel("Antall")

        plt.legend(frameon=False)
        self.__Ferdigstill()

    def FodselsOverskudd(self) -> None:
        df = self.df

        plt.figure(figsize=(16, 9))

        plt.plot(
            df["år"],
            df["fødselsoverskudd"],
            color=self.farge["lilla"],
            label="Fødselsover- og underskudd",
        )
        plt.axhline(y=0, linestyle="--", color=self.farge["kull"], alpha=0.6)
        plt.fill_between(
            df["år"],
            df["fødselsoverskudd"],
            0,
            where=(df["fødselsoverskudd"] > 0),
            color=self.farge["lyseGronn"],
            alpha=0.4,
            interpolate=True,
        )
        plt.fill_between(
            df["år"],
            df["fødselsoverskudd"],
            0,
            where=(df["fødselsoverskudd"] < 0),
            color=self.farge["lyseRod"],
            alpha=0.4,
            interpolate=True,
        )

        plt.plot(
            df["år"],
            self.analyse.LowessGlidendeRegresjon("fødselsoverskudd"),
            color=self.farge["morkRod"],
            label="Lowess (frac = 0.2)",
            alpha=0.7,
            linestyle=":",
            zorder=4,
        )

        xLim = plt.xlim()
        yLim = plt.ylim()

        # Tangent til glidende regresjon
        """
        sekantLowess = "fødselsoverskudd_sekant"
        self.analyse.LeggInnKolonne(sekantLowess, self.analyse.LowessGlidendeRegresjon("fødselsoverskudd"))
        dataSekant = self.analyse.SekantDiskret(sekantLowess, 2019, 2025)
        plt.plot(self.analyse.df["år"], dataSekant["linje"], 
                linestyle="-.",
                color="black",
                label=f"y = {dataSekant['a']:.2f}x {'+' if dataSekant['b'] > 0 else '-'} {abs(dataSekant['b']):.2f}")

        plt.scatter(dataSekant["x1"], dataSekant["y1"], 
                    label=f"({np.int64(dataSekant["x1"])}, {np.int64(dataSekant["y1"])})", color=self.farge["kull"], zorder=5)
        plt.scatter(dataSekant["x2"], dataSekant["y2"], 
                    label=f"({np.int64(dataSekant["x2"])}, {np.int64(dataSekant["y2"])})", color=self.farge["kull"], zorder=5)
        """

        plt.xlim(xLim)
        plt.ylim(yLim)
        plt.title(
            "Naturlig befolkningsvekst Verdal Kommune 1951 - 2025 (Levendefødte minus døde)"
        )
        plt.xlabel("År")
        plt.ylabel("Antall")

        plt.legend(frameon=False)
        self.__Ferdigstill()


    def InnOgUtflytting(self) -> None:
        df = self.df

        plt.figure()
        plt.plot(
            df["år"],
            df["innflytting"],
            color=self.farge["oliven"],
            label="Innflytting",
        )
        plt.plot(
            df["år"], df["utflytting"], 
            color=self.farge["rosa"], 
            label="Utflytting"
        )
        plt.fill_between(
            df["år"],
            df["utflytting"],
            df["innflytting"],
            where=df["innflytting"] > df["utflytting"],
            interpolate=True,
            color=self.farge["lyseGronn"],
            alpha=0.1
        )
        plt.fill_between(
            df["år"],
            df["innflytting"],
            df["utflytting"],
            where=df["utflytting"] > df["innflytting"],
            interpolate=True,
            color=self.farge["lyseRod"],
            alpha=0.1
        )
        # Aker etb
        """
        plt.axvline(x=1971.0, color=self.farge["kull"], 
                    label="Verftet åpnet (1969)", linestyle="--")
        plt.annotate("Etablering av verft (1969)", (1972, 910), color=self.farge["kull"])
        """

        plt.title("Inn- og utflytting Verdal Kommune 1951-2025")
        plt.xlabel("År")
        plt.ylabel("Antall")

        plt.legend(frameon=False, loc="upper left")
        self.__Ferdigstill() # plt.savefig(path)


    def NettoFlytting(self):
        df = self.df

        plt.figure(figsize=(16, 9))

        plt.plot(
            df["år"],
            df["netto_flytting"],
            color=self.farge["sand"],
            label="Netto flytting",
        )
        plt.axhline(y=0, linestyle="--", color=self.farge["kull"], alpha=0.6)
        plt.fill_between(
            df["år"],
            df["netto_flytting"],
            0,
            where=(df["netto_flytting"] > 0),
            color=self.farge["lyseGronn"],
            alpha=0.4,
            interpolate=True,
        )
        plt.fill_between(
            df["år"],
            df["netto_flytting"],
            0,
            where=(df["netto_flytting"] < 0),
            color=self.farge["lyseRod"],
            alpha=0.4,
            interpolate=True,
        )

        plt.plot(
            df["år"],
            self.analyse.LowessGlidendeRegresjon("netto_flytting"),
            color=self.farge["oliven"],
            label="Lowess frac=0.2",
            alpha=0.7,
            linestyle=":",
        )

        plt.title("Nettoflytting Verdal Kommune 1951 - 2025")
        plt.xlabel("År")
        plt.ylabel("Antall")

        plt.legend(frameon=False)
        self.__Ferdigstill()


    def StatistikkTabell(self) -> None:
        df = self.df.copy()  # Unngå mutasjon på original df

        opprinneligeKolonner = ["fødte", "døde", "netto_flytting", "folketilvekst"]
        
        stats = df[opprinneligeKolonner].describe()
        verdier = stats.loc[["mean", "std", "min", "25%", "75%", "max"]].round(1)
        
        # Beregn CV (Standardavvik / Gjennomsnitt) for hver kolonne
        cvRad = (stats.loc["std"] / stats.loc["mean"]).round(2)
        verdier.loc["CV"] = cvRad


        # Legger inn "statistikk i toppen"
        verdier = verdier.reset_index().rename(columns={"index": "Statistikk"})
        verdier["Statistikk"] = verdier["Statistikk"].str.upper() 

        kolonneTitel = [navn.replace("_", "").title() for navn in opprinneligeKolonner]
        header = ["Statistikk"] + kolonneTitel 

        plt.figure()
        plt.axis("off")

        tabell = plt.table(
            cellText=verdier.values,
            colLabels=header,
            loc="center",
            cellLoc="center",
        )

        tabell.auto_set_font_size(False)
        tabell.set_fontsize(8.5)
        tabell.scale(1, 1.6)

        # damearbeid
        for j in range(len(header)):
            tabell[(0, j)].set_facecolor(self.farge["morkBla"])
            tabell[(0, j)].set_text_props(color="white", fontweight="bold")

        
        for i in range(1, len(verdier) + 1):
            for j in range(len(header)):
                tabell[(i, j)].set_facecolor(
                    self.farge["blaHvit"] if i % 2 == 0 else "white"
                )

        self.__Ferdigstill()






    def DekadeStatistikkTabell(self) -> None:
        df = self.df.copy() # .copy() for å slippe referanse(ptr) til df

        # interpolerer resultatet 1.juli, for å kompensere for at folk dør
        # Bruker 31.des for å med 2025
        df["befolkning_31des"] = df["befolkning"] + df["fødte"] - df["døde"] + df["netto_flytting"]
        df["middelbefolkning"] = df["befolkning"] + df["befolkning_31des"] / 2

        df["dekade"] = (df["år"] // 10) * 10
        gruppe = df.groupby("dekade", as_index=False)[
            ["fødte", "døde", "netto_flytting", "folketilvekst", "middelbefolkning"]
        ].sum()


        gruppe["fødsels_prosent"] = gruppe["fødte"] / gruppe["middelbefolkning"] * 100
        gruppe["døde_prosent"] = gruppe["døde"] / gruppe["middelbefolkning"] * 100
        gruppe["flytte_prosent"] = gruppe["netto_flytting"] / gruppe["middelbefolkning"] * 100
        gruppe["folketilvekst_prosent"] = gruppe["folketilvekst"] / gruppe["middelbefolkning"] * 100

        kolonnerTilTabell = [
            "dekade",
            "fødsels_prosent",
            "døde_prosent",
            "flytte_prosent",
            "folketilvekst_prosent",
        ]
        gruppe = gruppe[kolonnerTilTabell]

        # Tabellformatering
        gruppe = gruppe.round(2)
        gruppe["dekade"] = gruppe["dekade"].astype(int).astype(str)
        kolonnerProsent = [
            "fødsels_prosent",
            "døde_prosent",
            "flytte_prosent",
            "folketilvekst_prosent",
        ]
        for kol in kolonnerProsent:
            gruppe[kol] = gruppe[kol].astype(str) + "%"

        header = [
            "Tiår",
            "Andel fødte",
            "Andel døde",
            "Andel flyttet",
            "Folketilvekst",
        ]

        plt.figure()
        plt.axis("off")


        tabell = plt.table(
            cellText=gruppe.values,
            colLabels=header,
            loc="center",
            cellLoc="center",
        )
        tabell.auto_set_font_size(False)
        tabell.set_fontsize(8.5)
        tabell.scale(1, 1.6)

        # fargelegging
        for j in range(len(header)):
            tabell[(0, j)].set_facecolor(self.farge["morkBla"])
            tabell[(0, j)].set_text_props(color="white", fontweight="bold")

        for i in range(1, len(gruppe) + 1):
            for j in range(len(header)):
                tabell[(i, j)].set_facecolor(
                    self.farge["blaHvit"] if i % 2 == 0 else "white"
                )

        self.__Ferdigstill()



    def IllustrerStandardavvik(self) -> None:
        df = self.df
        std = self.df[["fødte", "døde", "innflytting", "utflytting"]].std()
        mean = self.df[["fødte", "døde", "innflytting", "utflytting"]].mean()
        # self.__Ferdigstill()



    def TegnAlleGrafer(self) -> None:
        Logg(self, "Tegner alle grafer...")
        for navn in dir(self):
            if not navn.startswith("_") and navn.lower() != "tegnallegrafer":
                metode = getattr(self, navn)
                if callable(metode):
                    metode()
