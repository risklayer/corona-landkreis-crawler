#!/usr/bin/python3
from botbase import *

def ostalb(sheets):
    data = get_json("https://services7.arcgis.com/qBm3dGfAio0LQTV7/arcgis/rest/services/StatistikLR/FeatureServer/0/query?where=DATUM<%3D'"+today().strftime("%Y-%m-%d")+"'&outFields=*&orderByFields=Datum+DESC&resultRecordCount=2&f=json")
    data = data["features"]
    for k,v in data[0]["attributes"].items(): print(k,v,sep="\t")
    date = check_date(data[0]["attributes"]["Datum_Update"], "Ostalbkreis")
    c, cc = data[0]["attributes"]["Gesamtfälle"], data[1]["attributes"]["Gesamtfälle"]
    d, dd = data[0]["attributes"]["Anzahl_der_Verstorbenen"], data[1]["attributes"]["Anzahl_der_Verstorbenen"]
    g, gg = data[0]["attributes"]["Erkrankte__geheilt_aus_Isolatio"], data[1]["attributes"]["Erkrankte__geheilt_aus_Isolatio"]
    s = data[0]["attributes"]["Anzahl_Covid_19_Patienten_in_de"]
    cc, dd, gg = c - cc, d - dd, g - gg
    c, g = c + 194, g + 194
    # TODO: Impfungen auch?
    update(sheets, 8136, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, s=s, sig="Bot", comment="Bot", date=date)
    return True

schedule.append(Task(9, 00, 11, 30, 300, ostalb, 8136))
if __name__ == '__main__': ostalb(googlesheets())
