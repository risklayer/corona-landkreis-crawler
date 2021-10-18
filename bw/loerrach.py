#!/usr/bin/python3
from botbase import *

def loerrach(sheets):
    data = get_json('https://gis.loerrach-landkreis.de/arcgis/rest/services/AGOL/Corona/FeatureServer/1/query?f=json&where=1%3D1&outFields=*&returnGeometry=false')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Datum"], "Lörrach", datetime.timedelta(hours=6))
    c, cc = data["Befunde_positiv"], data["Befunde_positiv_Zuwachs"]
    d, dd = data["verstorben"], data["verstorben_Zuwachs"]
    a, aa = data["Faelle_aktiv"], data["Faelle_aktiv_Zuwachs"]
    s, i = data["Krankenhaus"], data["intensiv"]
    g, gg = c - d - a, cc - dd - aa
    q = a + data["Befunde_negativ"]
    update(sheets, 8336, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, s=s, i=i, sig="Bot", date=date)
    return True

schedule.append(Task(15, 15, 17, 10, 300, loerrach, 8336))
if __name__ == '__main__': loerrach(googlesheets())
