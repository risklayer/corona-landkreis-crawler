#!/usr/bin/python3
from botbase import *

def hohenlohe(sheets):
    data = get_json("https://gdi-hohenlohekreis.de/server/rest/services/public/SORMAS/FeatureServer/3/query?where=1%3D1&outFields=*&returnGeometry=false&f=json")
    #for k,v in data["features"][0]["attributes"].items(): print(k,v,sep="\t")
    date = dateutil.parser.parse(data["features"][0]["attributes"]["lga_stand"], dayfirst=True)
    date = check_date(date, "Hohenlohekreis", datetime.timedelta(hours=10))
    date = dateutil.parser.parse(data["features"][0]["attributes"]["dashboard_stand"], dayfirst=True)
    date = check_date(date, "Hohenlohekreis")
    data = get_json("https://gdi-hohenlohekreis.de/server/rest/services/public/SORMAS/FeatureServer/5/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=*&returnGeometry=false&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&gdbVersion=&historicMoment=&returnDistinctValues=false&returnIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=%5B%7B%22onStatisticField%22%3A%22ix_gesamt%22%2C%22outStatisticFieldName%22%3A%22ix_gesamt%22%2C%22statisticType%22%3A%22sum%22%7D%2C%0D%0A%7B%22onStatisticField%22%3A%22ix_neu%22%2C%22outStatisticFieldName%22%3A%22ix_neu%22%2C%22statisticType%22%3A%22sum%22%7D%2C%7B%22onStatisticField%22%3A%22ix_genesen%22%2C%22outStatisticFieldName%22%3A%22ix_genesen%22%2C%22statisticType%22%3A%22sum%22%7D%2C%7B%22onStatisticField%22%3A%22ix_verstorben%22%2C%22outStatisticFieldName%22%3A%22ix_verstorben%22%2C%22statisticType%22%3A%22sum%22%7D%2C%7B%22onStatisticField%22%3A%22k1_aktiv%22%2C%22outStatisticFieldName%22%3A%22k1_aktiv%22%2C%22statisticType%22%3A%22sum%22%7D%5D&returnZ=false&returnM=false&multipatchOption=xyFootprint&resultOffset=&resultRecordCount=&returnTrueCurves=false&returnExceededLimitFeatures=false&quantizationParameters=&returnCentroid=false&sqlFormat=none&resultType=&featureEncoding=esriDefault&datumTransformation=&f=pjson")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    c, cc = data["ix_gesamt"], data["ix_neu"]
    g, d = data["ix_genesen"], data["ix_verstorben"]
    #q = c - g - d + data["k1_aktiv"]
    update(sheets, 8126, c=c, cc=cc, g=g, d=d, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(9, 00, 16, 30, 300, hohenlohe, 8126))
if __name__ == '__main__': hohenlohe(googlesheets())
