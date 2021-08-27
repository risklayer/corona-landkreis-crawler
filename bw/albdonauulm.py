#!/usr/bin/python3
from botbase import *

def albdonauulm(sheets):
    import datetime, dateutil.parser
    data = get_json("https://services8.arcgis.com/rfTkYxW18pzySEF0/ArcGIS/rest/services/Coronadaten_fuer_Dashboard_1_Kreise/FeatureServer/0?f=json")
    date = datetime.datetime.utcfromtimestamp(data["editingInfo"]["lastEditDate"] / 1000.)
    if date.date() < datetime.date.today(): raise Exception("Alb-Donau-Ulm noch alt: "+str(date))
    data = get_json("https://services8.arcgis.com/rfTkYxW18pzySEF0/arcgis/rest/services/Coronadaten_fuer_Dashboard_1_Kreise/FeatureServer/0/query?where=1%3D1&outFields=*&orderByFields=KREIS_NAME+asc&f=json")
    data1 = data["features"][0]["attributes"]
    data2 = data["features"][1]["attributes"]
    #for k,v in data1.items(): print(k,v,sep="\t")
    ags = 8425 # Alb-Donau
    c, cc = data1["Fallzahl_Gesamt"], data1["Neuinfektionen_zum_Vortag"]
    g, d = data1["Genesene"], data1["Todesfaelle"]
    update(sheets, ags, c=c, cc=cc, g=g, d=d, sig="Bot", ignore_delta=True)
    ags = 8421 # Ulm
    c, cc = data2["Fallzahl_Gesamt"], data2["Neuinfektionen_zum_Vortag"]
    g, d = data2["Genesene"], data2["Todesfaelle"]
    update(sheets, ags, c=c, cc=cc, g=g, d=d, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(16, 00, 17, 30, 360, albdonauulm, 8421))
if __name__ == '__main__': albdonauulm(googlesheets())
