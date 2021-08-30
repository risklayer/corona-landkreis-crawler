#!/usr/bin/python3
from botbase import *

def heilbronnlk(sheets):
    data = get_json("https://services.arcgis.com/XUIQq0C4I0YmPJjS/arcgis/rest/services/CoronaLK_alles/FeatureServer/0/query?f=json&resultRecordCount=1&where=1%3D1&orderByFields=Datum%20DESC&outFields=*&returnGeometry=false")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Datum"], "LKHeilbronn")
    c, cc = data["GESAMT"], data["GESAMT_V"]
    d, dd = data["TOT"], data["TOT_V"]
    g, gg = data["GESUNDET"], data["GESUNDET_V"]
    cc, dd, gg = c - cc, d - dd, g - gg
    update(sheets, 8125, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(15, 30, 18, 30, 360, heilbronnlk, 8125))
if __name__ == '__main__': heilbronnlk(googlesheets())
