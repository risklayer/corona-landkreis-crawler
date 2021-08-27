#!/usr/bin/python3
from botbase import *

def sbk(sheets):
    import datetime
    data = get_json("https://services2.arcgis.com/iun1VzVHmraKymYG/ArcGIS/rest/services/Covid_19_Dashboard/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&resultRecordCount=1&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    ags, date = 8326, data["DATUMZAHL"]
    date = datetime.date(year=date//10000, month=(date//100)%100, day=date%100)
    if date < datetime.date.today(): raise Exception("SBK noch alt: "+str(date))
    date = date.strftime("%d.%m.%Y")
    c, cc = data["INF_LRASBK"], data["INF_NEU_LRASBK"]
    d, dd = data["TOTE_LRASBK"], data["TOTE_NEU_LRASBK"]
    g, gg = data["GENESEN_LRASBK"], data["GENESEN_NEU_LRASBK"]
    #data2 = get_json("")["features"]
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", comment="Bot OHNE S", date=date)
    return True

schedule.append(Task(9, 00, 10, 30, 300, sbk, 8326))
if __name__ == '__main__': sbk(googlesheets())
