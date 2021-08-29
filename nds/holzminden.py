#!/usr/bin/python3
from botbase import *

def holzminden(sheets):
    data = get_json("https://services6.arcgis.com/QuVJyRN01Ahxb5UI/arcgis/rest/services/Sicht_auf_Lagemeldung_Landkreis_ab_Nov2020/FeatureServer/0/query?f=json&resultRecordCount=1&where=1%3D1&orderByFields=datum_auswaehlen%20desc&outFields=*&returnGeometry=false")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["datum_auswaehlen"], "Holzminden")
    c, cc = data["bestaetigte_infektionen_landkreis_ges"], data["veraenderung_vormeldetag_gesamt"]
    d = data["todesfaelle_covid19_landkreis_ges"]
    g, gg = data["genesene_personen_landkreis_ges"], data["veraenderung_vormeldetag_genesen"]
    update(sheets, 3255, c=c, cc=cc, g=g, gg=gg, d=d, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(15, 0, 17, 30, 360, holzminden, 3255))
if __name__ == '__main__': holzminden(googlesheets())
