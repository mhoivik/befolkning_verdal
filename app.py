from dataHenter import DataHenter

class App:
    def Finnes(self, filnavn):
        try:
            open(filnavn).close()
            return True
        except:
            return False

    
    def Run(self):
        if not self.Finnes("data.csv"):
            if not self.Finnes("ubehandlet_data"):
                print("mangler filer!!")
                return
            print("\033[94mFant ikke data.csv, lager den...\033[0m")
            stiUsorterData = r"ubehandlet_data.csv"
            df = DataHenter(stiUsorterData).FormaterData()
            df.to_csv("data.csv")
        else:
            print("\033[94mFant data.csv\033[0m")

            

