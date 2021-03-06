#!/usr/bin/python3
from botbase import *

def rbk(sheets):
    data = get_json('https://services.arcgis.com/r7GhuZjF2UKLvKNF/arcgis/rest/services/CoronavirusSituation_CoronavirusSituation_View/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&groupByFieldsForStatistics=Date&outStatistics=[{"onStatisticField"%3A"confirmed"%2C"outStatisticFieldName"%3A"confirmed"%2C"statisticType"%3A"sum"}%2C%0D%0A{"onStatisticField"%3A"development"%2C"outStatisticFieldName"%3A"development"%2C"statisticType"%3A"sum"}%2C{"onStatisticField"%3A"recovered"%2C"outStatisticFieldName"%3A"recovered"%2C"statisticType"%3A"sum"}%2C{"onStatisticField"%3A"death"%2C"outStatisticFieldName"%3A"death"%2C"statisticType"%3A"sum"}%2C{"onStatisticField"%3A"quarantine"%2C"outStatisticFieldName"%3A"quarantine"%2C"statisticType"%3A"sum"}]&f=json')
    data = data["features"][0]["attributes"]
    # for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Date"], "RBK", datetime.timedelta(hours=6))
    c, cc = data["confirmed"], data["development"]
    d, q = data["death"], data["quarantine"]
    update(sheets, 5378, c=c, cc=cc, g=g, d=d, sig="Bot", comment="Bot Dashboard", date=date)
    return True

schedule.append(Task(12, 00, 14, 30, 360, rbk, 5378))
if __name__ == '__main__': rbk(googlesheets())
