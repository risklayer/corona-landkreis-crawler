#!/usr/bin/python3
from botbase import *

def muelheim(sheets):
    data = get_json("https://services-eu1.arcgis.com/qDRC9h4xkwtZ3Efs/arcgis/rest/services/Coronazahlen_Buerger/FeatureServer/1/query?where=1%3D1&outFields=*&orderByFields=DATUM+DESC&resultRecordCount=3&f=json")
    data1, data2 = data["features"][1]["attributes"], data["features"][2]["attributes"]
    #for k,v in data1.items(): print(k,v,sep="\t")
    date = check_date(data1["Datum"], "Mühlheim")
    c, cc = data1["Anzahl_Fae"], data2["Anzahl_Fae"]
    d, dd = data1["Anzahl_Ver"], data2["Anzahl_Ver"]
    g, gg = data1["Anzahl_P_1"], data2["Anzahl_P_1"]
    cc, dd, gg = c - cc, d - dd, g - gg
    q = data1["Anzahl_Qua"]
    update(sheets, 5117, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, sig="Bot", date=date, ignore_delta=False)
    return True

schedule.append(Task(7, 30, 10, 0, 180, muelheim, 5117))
if __name__ == '__main__': muelheim(googlesheets())
