#!/usr/bin/python3
from botbase import *

def lippe(sheets):
    import datetime, locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    qdatum = datetime.date.today().strftime("%d. %b. %Y")
    data = get_json("https://services-eu1.arcgis.com/H1pvqvVi8lTTXlkG/arcgis/rest/services/Verlauf_Lippe2/FeatureServer/0/query?where=1%3D1&outFields=*&orderByFields=Infizierte+DESC&resultRecordCount=2&f=json")
    data1 = data["features"][0]["attributes"]
    data2 = data["features"][1]["attributes"]
    #for k,v in data1.items(): print(k,v,sep="\t")
    if data1["Datum"] != qdatum: raise Exception("Lippe noch alt? "+data1["Datum"]+" expected "+qdatum)
    ags = 5766
    c, d, g = data1["Infizierte"], data1["Verstorbene"], data1["Gesunde"]
    cc, dd, gg = data2["Infizierte"], data2["Verstorbene"], data2["Gesunde"]
    cc, dd, gg = c - cc, d - dd, g - gg
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot")
    return True

schedule.append(Task(9, 50, 11, 30, 300, lippe, 5766))
if __name__ == '__main__': lippe(googlesheets())
