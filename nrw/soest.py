#!/usr/bin/python3
from botbase import *

def soest(sheets):
    data = get_json('https://gis.kreis-soest.de/server/rest/services/Krisenstab/Corona_Dashboard_Kreis_Soest_Oeffentlich/MapServer/2/query?where=1%3D1&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&having=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=Q__timestamp&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22bestaetigte%22%2C%22outStatisticFieldName%22%3A%22bestaetigte%22%7D%2C%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22bestaetigte_differenz%22%2C%22outStatisticFieldName%22%3A%22bestaetigte_differenz%22%7D%2C%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22lila%22%2C%22outStatisticFieldName%22%3A%22todesfaelle%22%7D%2C%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22todesfaelle_differenz%22%2C%22outStatisticFieldName%22%3A%22todesfaelle_differenz%22%7D%2C%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22dunkelgruen%22%2C%22outStatisticFieldName%22%3A%22genesene%22%7D%2C%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22genesene_differenz%22%2C%22outStatisticFieldName%22%3A%22genesene_differenz%22%7D%2C%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22hellblau%22%2C%22outStatisticFieldName%22%3A%22hellblau%22%7D%5D&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=json')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = data["Q__timestamp"]
    if not today().strftime("%d.%m.%Y") in date: raise NotYetAvailableException("Soest noch alt: "+str(date))
    c, cc = data["bestaetigte"], force_int(data["bestaetigte_differenz"])
    d, dd = data["todesfaelle"], force_int(data["todesfaelle_differenz"])
    g, gg = data["genesene"], force_int(data["genesene_differenz"])
    # k.A. was hellblau ist - intensiv?
    update(sheets, 5974, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", comment="Bot Dashboard ohne SI", date=date, ignore_delta=True)
    return True

schedule.append(Task(15, 30, 18, 30, 360, soest, 5974))
if __name__ == '__main__': soest(googlesheets())
