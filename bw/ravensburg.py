#!/usr/bin/python3
from botbase import *

def ravensburg(sheets):
    data = get_json("https://services5.arcgis.com/cjkDlTDV64UG3dg9/arcgis/rest/services/Corona_Dashboard_neu/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outStatistics=[{%22onStatisticField%22%3A%22stand%22%2C%22outStatisticFieldName%22%3A%22stand%22%2C%22statisticType%22%3A%22max%22}%2C{%22onStatisticField%22%3A%22verst%22%2C%22outStatisticFieldName%22%3A%22verst%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22geheilt%22%2C%22outStatisticFieldName%22%3A%22geheilt%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22Anzahl%22%2C%22outStatisticFieldName%22%3A%22Anzahl%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22dif%22%2C%22outStatisticFieldName%22%3A%22dif%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22gesund_dif%22%2C%22outStatisticFieldName%22%3A%22gesund_dif%22%2C%22statisticType%22%3A%22sum%22}]&f=json")
    data = data["features"][0]["attributes"]
    for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["stand"].replace(" UHR",""), "Ravensburg", datetime.timedelta(1))
    c, cc = data["Anzahl"], data["dif"]
    d = data["verst"]
    g, gg = data["geheilt"], data["gesund_dif"]
    update(sheets, 8436, c=c, cc=cc, g=g, gg=gg, d=d, sig="Bot", date=date, ignore_delta=True) #today().weekday()==0)
    return True

schedule.append(Task(15, 30, 18, 30, 300, ravensburg, 8436))
if __name__ == '__main__': ravensburg(googlesheets())
