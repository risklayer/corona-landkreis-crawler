#!/usr/bin/python3
from botbase import *

def essen(sheets):
    data = get_json("https://utility.arcgis.com/usrsvcs/servers/a2bd9c6789d64a1e9f5fce73ebd7a165/rest/services/essen/Covid19_Dashboard/MapServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&groupByFieldsForStatistics=STATUS&outStatistics=[{%22statisticType%22:%22sum%22,%22onStatisticField%22:%22ANZGES%22,%22outStatisticFieldName%22:%22sum%22},{%22statisticType%22:%22max%22,%22onStatisticField%22:%22DATEXP%22,%22outStatisticFieldName%22:%22DATEXP%22},{%22statisticType%22:%22max%22,%22onStatisticField%22:%22DATUM%22,%22outStatisticFieldName%22:%22DATUM%22}]&outFields=*")
    #for k,v in data["features"][0]["attributes"].items(): print(k,v,sep="\t")
    date = check_date(data["features"][0]["attributes"]["DATEXP"], "Essen", datetime.timedelta(hours=12))
    c, g, d = 0, 0, 0
    for f in data["features"]:
        f = f["attributes"]
        if f["STATUS"] == 3: c = f["sum"]
        if f["STATUS"] == 4: g = f["sum"]
        if f["STATUS"] == 5: d = f["sum"]
    date = data["features"][0]["attributes"]["DATEXP"]
    update(sheets, 5113, c=c, g=g, d=d, sig="Bot", comment="Bot Dashboard", date=date)
    return True

schedule.append(Task(8, 10, 20, 10, 1800, essen, 5113))
if __name__ == '__main__': essen(googlesheets())
