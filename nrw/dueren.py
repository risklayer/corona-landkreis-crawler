#!/usr/bin/python3
from botbase import *

def dueren(sheets):
    data = get_json("https://services-eu1.arcgis.com/B4AGMbvhuqY0JRyu/arcgis/rest/services/CoronaFallzahlenKreis/FeatureServer/0/query?f=json&where=1%3D1&outFields=*&returnGeometry=false")
    data = data["features"][0]["attributes"]
    # for k, v in data.items(): print(k, v, sep="\t")
    date = check_date(data["Datum"], "Düren")
    c, g, d = data["Summe"], data["Genesen"], data["Verstorben"]
    cc = data["Infektionsdelta_Vortag"]
    # TODO: Impfzahlen auch vorhanden!
    update(sheets, 5358, c=c, cc=cc, g=g, d=d, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(9, 30, 13, 10, 300, dueren, 5358))
if __name__ == '__main__': dueren(googlesheets())
