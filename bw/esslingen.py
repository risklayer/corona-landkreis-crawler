#!/usr/bin/python3
from botbase import *

def esslingen(sheets):
    data = get_json('https://services2.arcgis.com/mL26ZKdlhFJH9AoM/arcgis/rest/services/es_corona/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&orderByFields=dat_zahl+desc&groupByFieldsForStatistics=dat_zahl&outStatistics=[{"statisticType"%3A"sum"%2C"onStatisticField"%3A"inf_ges"%2C"outStatisticFieldName"%3A"inf_ges"}%2C{"statisticType"%3A"sum"%2C"onStatisticField"%3A"pers_qua"%2C"outStatisticFieldName"%3A"pers_qua"}]&resultRecordCount=2&f=json')["features"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = data[0]["attributes"]["dat_zahl"]
    date = datetime.date(year=date//10000, month=(date//100)%100, day=date%100) + datetime.timedelta(days=1)
    date = check_date(date, "Esslingen")
    c, cc = data[0]["attributes"]["inf_ges"], data[1]["attributes"]["inf_ges"]
    a, aa = data[0]["attributes"]["pers_qua"], data[1]["attributes"]["pers_qua"]
    data2 = get_json("https://services2.arcgis.com/mL26ZKdlhFJH9AoM/ArcGIS/rest/services/LGA_pandemie_daten_formel/FeatureServer/0/query?where=1%3D1&outFields=*&orderByFields=Meldedatum+DESC&resultRecordCount=2&f=json")["features"]
    d, dd = data2[0]["attributes"]["verstorben"], data2[1]["attributes"]["verstorben"]
    g, gg = c - a - d, cc - aa - dd # G berechnen
    cc, dd, gg = c - cc, d - dd, g -gg # Änderung
    update(sheets, 8116, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=today().weekday()==0) # ignore am Montag würde reichen
    return True

schedule.append(Task(9, 00, 10, 30, 300, esslingen, 8116))
if __name__ == '__main__': esslingen(googlesheets())
