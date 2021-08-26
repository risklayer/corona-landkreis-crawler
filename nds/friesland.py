#!/usr/bin/python3
from botbase import *

def friesland(sheets):
    data = get_json("https://services9.arcgis.com/NdRIoRRHq1CjkAY8/arcgis/rest/services/Covid19_Fallzahlen/FeatureServer/0/query?where=Datum%3C%3D%27"+time.strftime("%Y-%m-%d")+"%27&outFields=*&&orderByFields=Datum+DESC&resultRecordCount=1&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    ags, date = 3455, data["Datenaktualitaet"].replace(","," ")
    if not todaystr in date: raise Exception("Friesland noch alt")
    c, cc = data["Faelle_gesamt"], data["Faelle_gesamt_veraenderung"]
    d, dd = data["verstorben"], data["verstorben_veraenderung"]
    g, gg = data["genesen"], data["genesen_veraenderung"]
    q, s = data["Quarantaene_aktuell"], data["Faelle_stationaer"]
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, s=s, sig="Bot", date=date)
    return True

schedule.append(Task(15, 15, 17, 30, 360, friesland, 3455))
if __name__ == '__main__': friesland(googlesheets())
