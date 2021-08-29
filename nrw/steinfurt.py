#!/usr/bin/python3
from botbase import *

def steinfurt(sheets):
    data = get_json("https://services3.arcgis.com/oM2Afmj2Zc4sLdCw/arcgis/rest/services/Covid19_Fallzahlen/FeatureServer/0/query?f=json&where=KOMMUNE%3D'01%20-%20Kreis%20Steinfurt'&returnGeometry=false&outFields=*&orderByFields=DATUM%20desc&resultRecordCount=1")
    data = data["features"][0]["attributes"]
    # for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["DATUM"], "Steinfurt")
    date = data["STAND"].replace(",","")
    c, cc = data["INFIZIERTE_SUM"], data["INFIZIERTE"]
    d, dd = data["VERSTORBENE_SUM"], data["VERSTORBENE"]
    g, gg = data["GESUNDETE_SUM"], data["GESUNDETE"]
    update(sheets, 5566, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(18, 15, 19, 30, 180, steinfurt, 5566))
if __name__ == '__main__': steinfurt(googlesheets())
