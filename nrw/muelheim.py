#!/usr/bin/python3
from botbase import *

def muelheim(sheets):
    import datetime
    data = get_json("https://services-eu1.arcgis.com/qDRC9h4xkwtZ3Efs/arcgis/rest/services/Coronazahlen_Buerger/FeatureServer/1/query?where=1%3D1&outFields=*&orderByFields=DATUM+DESC&resultRecordCount=3&f=json")
    data1 = data["features"][1]["attributes"]
    data2 = data["features"][2]["attributes"]
    #for k,v in data1.items(): print(k,v,sep="\t")
    ags, date = 5117, datetime.datetime.utcfromtimestamp(data1["Datum"] / 1000)
    if date.date() < datetime.date.today(): raise Exception("Mühlheim noch alt: "+date)
    date = date.strftime("%d.%m.%Y")
    c, cc = data1["Anzahl_Fae"], data2["Anzahl_Fae"]
    d, dd = data1["Anzahl_Ver"], data2["Anzahl_Ver"]
    g, gg = data1["Anzahl_P_1"], data2["Anzahl_P_1"]
    cc, dd, gg = c - cc, d - dd, g - gg
    q = data1["Anzahl_Qua"]
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=False)
    return True

schedule.append(Task(9, 00, 10, 00, 180, muelheim, 5117))
if __name__ == '__main__': muelheim(googlesheets())
