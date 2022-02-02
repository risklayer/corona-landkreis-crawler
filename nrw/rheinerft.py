#!/usr/bin/python3
from botbase import *

def rheinerft(sheets):
    #data = get_json("https://services7.arcgis.com/lDivAOFOYuYRJqnX/arcgis/rest/services/REK_C19/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&f=json")
    data = get_json("https://services7.arcgis.com/lDivAOFOYuYRJqnX/ArcGIS/rest/services/Zeit_C19/FeatureServer/0/query?where=1%3D1&outFields=*&orderByFields=Datum+DESC&resultRecordCount=2&f=json")
    data1, data2 = data["features"][0]["attributes"], data["features"][1]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data1["Datum"], "Rhein-Erft")
    c, cc = data1["bestätigte_Fälle_insgesamt"], data2["bestätigte_Fälle_insgesamt"]
    d, dd = data1["Todesfälle"], data2["Todesfälle"]
    g, gg = data1["Genesen"], data2["Genesen"]
    q = data1["Personen_in_Quarantäne"]
    q = (q + c - d - g) if q else None
    cc, dd, gg = c - cc, d - dd, g - gg
    update(sheets, 5362, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, sig="Bot", comment="Bot Dashboard ohne SI", ignore_delta=True, date=date)
    return True

schedule.append(Task(17, 15, 21, 30, 360, rheinerft, 5362))
if __name__ == '__main__': rheinerft(googlesheets())
