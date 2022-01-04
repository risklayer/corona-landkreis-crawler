#!/usr/bin/python3
from botbase import *

def euskirchen(sheets):
    data = get_json("https://services2.arcgis.com/H89X5E4Qydz7zeBz/arcgis/rest/services/DB_COVID_19/FeatureServer/2/query?f=json&where=1%3D1&returnGeometry=false&outFields=*")
    data = data["features"][0]["attributes"]
    # for k,v in data.items(): print(k,v,sep="\t")
    if "2021" in data["Datum_TXT"]:
        date = check_date(data["Datum_TXT"], "Euskirchen", datetime.timedelta(365)) + datetime.timedelta(365)
    else:
        date = check_date(data["Datum_TXT"], "Euskirchen")
    c, cc = data["Faelle_insgesamt"], data["Faelle_insgesamt_Vortag"]
    d, dd = data["Todesfaelle_gesamt"], data["Todesfaelle_gesamt_Vortag"]
    a, aa = data["aktuell_positiv"], data["aktuell_positiv_Vortag"]
    g, gg = c - d - a, cc - dd - aa
    cc, dd, gg = c - cc, d - dd, g - gg
    update(sheets, 5366, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(13, 30, 16, 00, 300, euskirchen, 5366))
if __name__ == '__main__': euskirchen(googlesheets())
