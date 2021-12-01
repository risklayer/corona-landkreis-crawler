#!/usr/bin/python3
from botbase import *

def mainkinzig(sheets):
    data = get_json('https://services-eu1.arcgis.com/aQSRzlNSA0Mcrrk4/arcgis/rest/services/2021_DBMKK_Daten_Sicht/FeatureServer/0/query?where=1%3D1&outFields=*&outStatistics=[{"onStatisticField"%3A"Alle"%2C"outStatisticFieldName"%3A"Alle"%2C"statisticType"%3A"sum"}%2C{"onStatisticField"%3A"Neu"%2C"outStatisticFieldName"%3A"Neu"%2C"statisticType"%3A"sum"}%2C%0D%0A{"onStatisticField"%3A"NeuInf"%2C"outStatisticFieldName"%3A"NeuInf"%2C"statisticType"%3A"sum"}%2C{"onStatisticField"%3A"TF"%2C"outStatisticFieldName"%3A"TF"%2C"statisticType"%3A"sum"}%2C{"onStatisticField"%3A"Inz7"%2C"outStatisticFieldName"%3A"Inz7"%2C"statisticType"%3A"max"}]&f=json')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = data["Inz7"]
    if not today().strftime("%d.%m.%Y") in date: raise NotYetAvailableException("MKK noch alt: "+str(date))
    c, cc = data["Alle"], data["Neu"]
    d = data["TF"]
    g = c - d- data["NeuInf"]
    # TODO: Impfungen auch?
    update(sheets, 6435, c=c, cc=cc, g=g, d=d, sig="Bot", comment="Bot Dashboard", date=date, ignore_delta=True)
    return True

schedule.append(Task(13, 3, 21, 30, 600, mainkinzig, 6435))
if __name__ == '__main__': mainkinzig(googlesheets())
