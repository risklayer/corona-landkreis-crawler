#!/usr/bin/python3
from botbase import *

def tirschenreuth(sheets):
    data = get_json("https://services3.arcgis.com/fygSJbpgKmtJnuHJ/ArcGIS/rest/services/Corona_Fallmonitor_Dashboard_V02/FeatureServer/0/query?where=AGS%3D9377&outFields=*&orderByFields=Datum+desc&resultRecordCount=2&f=json")
    data2 = data["features"][1]["attributes"]
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Datum"], "Tirschenreuth")
    c, cc = data["Infektionen_insg"], data["Infektionen_Tag"]
    d, dd = data["Todesfälle_insg"], data2["Todesfälle_insg"]
    g, gg = data["Genesene_ins"], data2["Genesene_ins"]
    dd, gg = d - dd, g - gg
    update(sheets, 9377, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(11, 30, 17, 30, 900, tirschenreuth, 9377))
if __name__ == '__main__': tirschenreuth(googlesheets())
