#!/usr/bin/python3
from botbase import *

def dueren(sheets):
    data = get_json("https://services-eu1.arcgis.com/B4AGMbvhuqY0JRyu/arcgis/rest/services/CoronaFallzahlenKreis/FeatureServer/0/query?f=json&where=1%3D1&outFields=*&returnGeometry=false")
    data = data["features"][0]["attributes"]
    # for k, v in data.items(): print(k, v, sep="\t")
    #ags, date = 5358, datetime.datetime.utcfromtimestamp(data["Datum"] / 1000)
    #if date.date() < datetime.date.today(): raise Exception("Düren noch nicht aktuell")
    #date = date.strftime("%d.%m.%Y")
    date = check_date(data["Datum"], "Düren")
    c, g, d = data["Summe"], data["Genesen"], data["Verstorben"]
    cc = data["Infektionsdelta_Vortag"]
    # TODO: Impfzahlen auch vorhanden!
    update(sheets, 5358, c=c, cc=cc, g=g, d=d, sig="Bot", date=date)
    return True

schedule.append(Task(11, 55, 13, 10, 300, dueren, 5358))
if __name__ == '__main__': dueren(googlesheets())
