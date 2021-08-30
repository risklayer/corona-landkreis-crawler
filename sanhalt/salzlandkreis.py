#!/usr/bin/python3
from botbase import *

def salzlandkreis(sheets):
    data = get_json('https://services-eu1.arcgis.com/Llocydn9lKFsr3ys/arcgis/rest/services/Covid_neues_Dashboard/FeatureServer/6/query?f=json&cacheHint=true&resultOffset=0&resultRecordCount=1&where=1%3D1&orderByFields=Datum%20DESC&outFields=*&resultType=standard&returnGeometry=false&spatialRel=esriSpatialRelIntersects')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Datum"], "Salzlandkreis")
    c, cc = data["Faelle_G_1"], data["Faelle_Heu"]
    d, dd = data["Todesfaell"], data["Todesfae_1"]
    g = data["Faelle_G_3"] # Summe_Fa_1 - keine Ahung
    update(sheets, 15089, c=c, cc=cc, g=g, d=d, dd=dd, sig="", comment="Bot Dashboard, C später Land", date=date, ignore_delta=True, without_c=True)
    return True

schedule.append(Task(10, 00, 11, 30, 300, salzlandkreis, 15089))
if __name__ == '__main__': salzlandkreis(googlesheets())
