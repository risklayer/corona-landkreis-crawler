#!/usr/bin/python3
from botbase import *

def sbk(sheets):
    data = get_json("https://services2.arcgis.com/iun1VzVHmraKymYG/ArcGIS/rest/services/Covid_19_Dashboard/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&resultRecordCount=1&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["DATUMZAHL"], "SBK")
    c, cc = data["INF_LRASBK"], data["INF_NEU_LRASBK"]
    d, dd = data["TOTE_LRASBK"], data["TOTE_NEU_LRASBK"]
    g, gg = data["GENESEN_LRASBK"], data["GENESEN_NEU_LRASBK"]
    update(sheets, 8326, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", comment="Bot OHNE S", date=date)
    return True

schedule.append(Task(9, 00, 11, 30, 300, sbk, 8326))
if __name__ == '__main__': sbk(googlesheets())
