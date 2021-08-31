#!/usr/bin/python3
from botbase import *

def meissen(sheets):
    data = get_json("https://services3.arcgis.com/nuqf686aSQH6Su4v/arcgis/rest/services/CSV_Daten_zu_COVID/FeatureServer/0/query?where=1%3D1&outFields=*&orderByFields=Datum+DESC&resultRecordCount=1&f=json")
    data = data["features"][0]["attributes"]
    # for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Datum"], "Meissen", datetime.timedelta(hours=6))
    c, cc = data["Indexfälle_gesamt"], data["Neue_Indexfälle"]
    d, dd = data["Sterbefälle_gesamt"], data["Neue_Sterbefälle"]
    g = c - d - data["Aktive_Quarantäne"]
    update(sheets, 14627, c=c, cc=cc, g=g, d=d, dd=dd, sig="Bot", comment="Bot ohne QSI Dashboard", date=date, ignore_delta=True)
    return True

schedule.append(Task(11, 15, 12, 45, 180, meissen, 14627))
if __name__ == '__main__': meissen(googlesheets())
