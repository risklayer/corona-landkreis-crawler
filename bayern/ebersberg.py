#!/usr/bin/python3
from botbase import *

def ebersberg(sheets):
    data = get_json('https://services-eu1.arcgis.com/CZ1GXX3MIjSRSHoC/arcgis/rest/services/EBE_Landkreis_Inzidenztabelle/FeatureServer/0/query?where=1%3D1&outFields=*&outStatistics=[{%22onStatisticField%22%3A%22positiv_neu%22%2C%22outStatisticFieldName%22%3A%22positiv%22%2C%22statisticType%22%3A%22sum%22}%2C{"onStatisticField"%3A"Datum_Meldung"%2C"outStatisticFieldName"%3A"Datum_Meldung"%2C"statisticType"%3A"max"}]&f=json')
    c = data["features"][0]["attributes"]["positiv"]
    date = datetime.datetime.utcfromtimestamp(data["features"][0]["attributes"]["Datum_Meldung"] / 1000)
    filterdate = (date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    date = date + datetime.timedelta(days=1)
    #print(str(date), filterdate)
    # for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(date, "Ebersberg")
    data = get_json('https://services-eu1.arcgis.com/CZ1GXX3MIjSRSHoC/arcgis/rest/services/EBE_Gemeinden_Inzidenztabelle_3/FeatureServer/0/query?where=1%3D1&outFields=*&orderByFields=Datum_Meldung+DESC&groupByFieldsForStatistics=Datum_Meldung&outStatistics=[{"onStatisticField"%3A"positiv_neu"%2C"outStatisticFieldName"%3A"positiv_neu"%2C"statisticType"%3A"sum"}]&resultRecordCount=1&f=json')
    #print(data)
    cc = data["features"][0]["attributes"]["positiv_neu"]
    # D kommt vom RKI, aber wir brauchen es für G
    data = get_json('https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?f=json&cacheHint=true&resultOffset=0&resultRecordCount=1&where=GEN%3D%27Ebersberg%27&outFields=*&resultType=standard&returnGeometry=false&spatialRel=esriSpatialRelIntersects')
    d = data["features"][0]["attributes"]["deaths"]
    data = get_json("https://services-eu1.arcgis.com/CZ1GXX3MIjSRSHoC/arcgis/rest/services/Mutationen_Quarantaene/FeatureServer/0/query?f=json&outFields=*&outStatistics=[{%22onStatisticField%22%3A%22ObjectId%22%2C%22outStatisticFieldName%22%3A%22aktiv%22%2C%22statisticType%22%3A%22count%22}]&returnGeometry=false&where=EndeIsolation%3E%3Dtimestamp%20%27"+filterdate+"%2022%3A00%3A00%27")
    a = data["features"][0]["attributes"]["aktiv"]
    data = get_json("https://services-eu1.arcgis.com/CZ1GXX3MIjSRSHoC/arcgis/rest/services/Mutationen_Quarantaene/FeatureServer/0/query?f=json&outFields=*&outStatistics=[{%22onStatisticField%22%3A%22KP1aktiv%22%2C%22outStatisticFieldName%22%3A%22KP1aktiv%22%2C%22statisticType%22%3A%22sum%22}]&returnGeometry=false&where=KP1aktiv%3E0")
    #for k,v in data.items(): print(k,v,sep="\t")
    g = c - d - a
    q = data["features"][0]["attributes"]["KP1aktiv"] + a
    update(sheets, 9175, c=c, cc=cc, g=g, d=d, q=q, sig="Bot", comment="Bot Dashboard ohne SI", date=date, ignore_delta=True)
    return True

schedule.append(Task(15, 30, 18, 30, 600, ebersberg, 9175))
if __name__ == '__main__': ebersberg(googlesheets())
