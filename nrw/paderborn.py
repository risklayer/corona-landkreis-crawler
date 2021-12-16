#!/usr/bin/python3
from botbase import *

def paderborn(sheets):
    data = get_json("https://services2.arcgis.com/pnCpFE2nIdh1mSrn/arcgis/rest/services/CORONA_FALLZAHLEN_PROD/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["DATUM1"], "Paderborn")
    data = get_json("https://services2.arcgis.com/pnCpFE2nIdh1mSrn/arcgis/rest/services/CORONA_FALLZAHLEN_PROD/FeatureServer/2/query?where=GEM_NR%3D-2+AND+MAPDUMMY_S%3D%27n%27&outFields=*&returnGeometry=false&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    #date = check_date(data["DATUM"], "Paderborn")
    c, cc = data["BE_AKTUINT"], force_int(data["BE_DIF1INT"])
    d, dd = data["TO_AKTUINT"], force_int(data["TO_DIF1INT"])
    g, gg = data["GE_AKTUINT"], force_int(data["GE_DIF1INT"])
    update(sheets, 5774, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", comment="Bot Dashboard ohne QSI", ignore_delta=True, date=date)
    return True

schedule.append(Task(17, 0, 18, 30, 360, paderborn, 5774))
if __name__ == '__main__': paderborn(googlesheets())
