#!/usr/bin/python3
from botbase import *

def remsmurr(sheets):
    import datetime, dateutil.parser
    data = get_json("https://services5.arcgis.com/0bChhVBO7DpK81l8/arcgis/rest/services/Corona_Kennzahlen_Sicht/FeatureServer/0/query?f=json&where=1%3D1&outFields=*&returnGeometry=false")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    ags, date = 8119, data["Timedate"].replace(" Uhr","")
    if not todaystr in date: raise Exception("Remsmurr noch alt: "+str(date))
    c, cc = data["positivAll"], data["positivAllV"]
    d, dd = data["totAll"], data["totAllV"]
    g, gg = data["gesundAllV"], data["gesundAllV"]
    cc, dd, gg = c - cc, d - dd, g - gg
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date)
    return True

schedule.append(Task(16, 00, 17, 30, 360, remsmurr, 8119))
if __name__ == '__main__': remsmurr(googlesheets())
