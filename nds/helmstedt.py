#!/usr/bin/python3
from botbase import *

def helmstedt(sheets):
    data = get_json("https://services.arcgis.com/zu026cYG1eiMynLL/arcgis/rest/services/COVID_V2a_Kreis_Chronologie_SICHT/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&orderByFields=Datum+desc&resultRecordCount=2&f=json")
    data2 = data["features"][1]["attributes"]
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(datetime.datetime.utcfromtimestamp(data["Datum"]/1000), "Helmstedt", datetime.timedelta(hours=3))
    data3 = get_json("https://services.arcgis.com/zu026cYG1eiMynLL/arcgis/rest/services/COVID_V2a_Werte_Sicht1/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&f=json")
    c, cc = data["bisher_infiziert"], data2["bisher_infiziert"]
    d, dd = data["Todesfaelle"], data2["Todesfaelle"]
    g, gg = data["genesen"], data2["genesen"]
    cc, dd, gg = c - cc, d - dd, g - gg
    q = data3["features"][0]["attributes"]["Quarantaene"] + c - d - g
    #q = data["Quarantaene"] + data["derzeit_krank"]
    # TODO: Impfungen auch?
    update(sheets, 3154, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, sig="Bot", date=date)
    return True

schedule.append(Task(14, 30, 17, 30, 300, helmstedt, 3154))
if __name__ == '__main__': helmstedt(googlesheets())
