#!/usr/bin/python3
from botbase import *

def zak(sheets):
    data = get_json("https://services3.arcgis.com/5oPkDqFNiQRoI8BR/arcgis/rest/services/Zollernalbkreis_Corona_Dashboard_AGO/FeatureServer/5/query?where=1%3D1&outFields=*&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    #ags, date = 8417, datetime.datetime.fromtimestamp(data["Datum"] / 1000)
    date = check_date(data["Datum"], "Zollernalbkreis")
    #if date.date() < datetime.date.today(): raise Exception("ZAK noch alt: "+str(date))
    #date = date.strftime("%d.%m.%Y")
    mit = data["Todesfaelle_mit_Covid"]
    c = data["Infizierte"]
    d = data["Verstorbene"] + mit
    g = data["Genesene"] - mit
    idata = get_json("https://services3.arcgis.com/5oPkDqFNiQRoI8BR/arcgis/rest/services/Zollernalbkreis_Corona_Dashboard_AGO/FeatureServer/7/query?where=1%3D1&outFields=*&f=json")
    idata = idata["features"][0]["attributes"]
    s = idata["Gesamt1"] + idata["Gesamt2"]
    i = idata["Intensiv1"] + idata["Intensiv2"]
    update(sheets, 8417, c=c, g=g, d=d, s=s, i=i, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(16, 30, 18, 30, 300, zak, 8417))
if __name__ == '__main__': zak(googlesheets())
