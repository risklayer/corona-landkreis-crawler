#!/usr/bin/python3
from botbase import *

def essen(sheets):
    #data = get_json("https://utility.arcgis.com/usrsvcs/servers/a2bd9c6789d64a1e9f5fce73ebd7a165/rest/services/essen/Covid19_Dashboard/MapServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&groupByFieldsForStatistics=STATUS&outStatistics=[{%22statisticType%22:%22sum%22,%22onStatisticField%22:%22ANZGES%22,%22outStatisticFieldName%22:%22ANZGES%22},{%22statisticType%22:%22max%22,%22onStatisticField%22:%22DATEXP%22,%22outStatisticFieldName%22:%22DATEXP%22},{%22statisticType%22:%22max%22,%22onStatisticField%22:%22DATUM%22,%22outStatisticFieldName%22:%22DATUM%22},{%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22ANZAKT%22%2C%22outStatisticFieldName%22%3A%22ANZAKT%22}]&outFields=*")
    data = get_json("https://utility.arcgis.com/usrsvcs/servers/a2bd9c6789d64a1e9f5fce73ebd7a165/rest/services/essen/Covid19_Dashboard/MapServer/8/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&groupByFieldsForStatistics=DATUM&outStatistics=[{%22statisticType%22:%22sum%22,%22onStatisticField%22:%22KUMULIERT_POSITIVE%22,%22outStatisticFieldName%22:%22KUMULIERT_POSITIVE%22},{%22statisticType%22:%22sum%22,%22onStatisticField%22:%22KUMULIERT_VERSTORBENE%22,%22outStatisticFieldName%22:%22KUMULIERT_VERSTORBENE%22},{%22statisticType%22:%22sum%22,%22onStatisticField%22:%22KUMULIERT_ENTISOLIERTE%22,%22outStatisticFieldName%22:%22KUMULIERT_ENTISOLIERTE%22},{%22statisticType%22:%22sum%22,%22onStatisticField%22:%22AKTIVE_QUARANTAENEN%22,%22outStatisticFieldName%22:%22AKTIVE_QUARANTAENEN%22}]&resultOffset=0&resultRecordCount=1&orderByFields=DATUM+DESC")
    #for k,v in data["features"][0]["attributes"].items(): print(k,v,sep="\t")
    dat = data["features"][0]["attributes"]
    date = check_date(dat["DATUM"], "Essen", datetime.timedelta(hours=-12))
    c = dat["KUMULIERT_POSITIVE"]
    d = dat["KUMULIERT_VERSTORBENE"]
    g = dat["KUMULIERT_ENTISOLIERTE"]
    q = dat["AKTIVE_QUARANTAENEN"] + c - d - g
    update(sheets, 5113, c=c, g=g, d=d, q=q, sig="Vorläufig", comment="Dashboard ohne SI, leichte Abw", date=date, ignore_delta=True)
    return True

schedule.append(Task(8, 10, 20, 10, 1800, essen, 5113))
if __name__ == '__main__': essen(googlesheets())
