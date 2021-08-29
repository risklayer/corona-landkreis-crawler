#!/usr/bin/python3
from botbase import *

def friesland(sheets):
    data = get_json("https://services9.arcgis.com/NdRIoRRHq1CjkAY8/arcgis/rest/services/Covid19_Fallzahlen/FeatureServer/0/query?where=Datum%3C%3D%27"+today().strftime("%Y-%m-%d")+"%27&outFields=*&&orderByFields=Datum+DESC&resultRecordCount=1&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = data["Datenaktualitaet"].replace(","," ")
    if not today().strftime("%d.%m.%Y") in date: raise NotYetAvailableException("Friesland noch alt")
    c, cc = int(data["Faelle_gesamt"]), int(data["Faelle_gesamt_Veraenderung"])
    d, dd = int(data["verstorben"]), int(data["verstorben_Veraenderung"])
    g, gg = int(data["genesen"]), int(data["genesen_Veraenderung"])
    q, s = int(data["Quarantaene_aktuell"]), int(data["Faelle_stationaer"])
    update(sheets, 3455, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, s=s, sig="Bot", date=date)
    return True

schedule.append(Task(15, 15, 17, 30, 360, friesland, 3455))
if __name__ == '__main__': friesland(googlesheets())
