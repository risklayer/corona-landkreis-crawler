#!/usr/bin/python3
from botbase import *

def salzgitter(sheets):
    data = get_json("https://services7.arcgis.com/trmg2NhJbLzZxYMC/arcgis/rest/services/Corona_Fallzahlen_Stadt_Salzgitter_View/FeatureServer/0/query?f=json&resultRecordCount=1&where=Stadtteil%3D'Stadt+Salzgitter'&orderByFields=Datum+DESC&outFields=*&returnGeometry=false")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Datum"], "Salzgitter", datetime.timedelta(1)) + datetime.timedelta(1)
    c, cc = data["Gesamt"], data["Differenz_Gesamt"]
    d, a = data["Verstorben"], data["aktuelle_Infektionen"]
    g = c - d - a
    update(sheets, 3102, c=c, cc=cc, g=g, d=d, sig="Bot", date=date, ignore_delta=False)
    return True

schedule.append(Task(9, 00, 11, 30, 360, salzgitter, 3102))
if __name__ == '__main__': salzgitter(googlesheets())
