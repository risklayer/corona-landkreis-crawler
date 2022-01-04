#!/usr/bin/python3
from botbase import *

def friesland(sheets):
    tomorrow = today() + datetime.timedelta(1)
    data = get_json("https://services9.arcgis.com/NdRIoRRHq1CjkAY8/arcgis/rest/services/Covid19_Fallzahlen/FeatureServer/0/query?where=Datum%3C%3D%27"+tomorrow.strftime("%Y-%m-%d")+"%27&outFields=*&&orderByFields=Datum+DESC&resultRecordCount=1&f=json")
    #print(data)
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = data["Datenaktualitaet"].replace(","," ")
    date = date.split(".")
    date = date[0] + "." + date[1] + "." + date[2] + (":" + date[3] if len(date)>3 else "")
    date = check_date(date, "Friesland")
    #if not today().strftime("%d.%m.%Y") in date: raise NotYetAvailableException("Friesland noch alt")
    c, cc = int(data["Faelle_gesamt"]), int(data["Faelle_gesamt_Veraenderung"])
    d, dd = int(data["verstorben"]), int(data["verstorben_Veraenderung"])
    g, gg = int(data["genesen"]), int(data["genesen_Veraenderung"])
    q, s = int(data["Quarantaene_aktuell"]), int(data["Faelle_stationaer"])
    update(sheets, 3455, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, s=s, sig="Bot", date=date, ignore_delta=True) # delta am WE falsch?
    return True

schedule.append(Task(13, 30, 17, 30, 360, friesland, 3455))
if __name__ == '__main__': friesland(googlesheets())
