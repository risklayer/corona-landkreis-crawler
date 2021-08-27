#!/usr/bin/python3
from botbase import *

def loerrach(sheets):
    import datetime
    data = get_json('https://gis.loerrach-landkreis.de/arcgis/rest/services/AGOL/Corona/FeatureServer/1/query?f=json&where=1%3D1&outFields=*&returnGeometry=false')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    ags, date = 8336, datetime.datetime.utcfromtimestamp(data["Datum"]/1000)
    if date.date() < datetime.date.today(): raise Exception("Lörrach noch alt: "+str(date))
    date = date.strftime("%d.%m.%Y")
    c, cc = data["Befunde_positiv"], data["Befunde_positiv_Zuwachs"]
    d, dd = data["verstorben"], data["verstorben_Zuwachs"]
    a, aa = data["Faelle_aktiv"], data["Faelle_aktiv_Zuwachs"]
    s, i = data["Krankenhaus"], data["intensiv"]
    g, gg = c - d - a, cc - dd - aa
    q = a + data["Befunde_negativ"]
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, s=s, i=i, sig="Bot", date=date)
    return True

schedule.append(Task(15, 25, 16, 10, 300, loerrach, 8336))
if __name__ == '__main__': loerrach(googlesheets())
