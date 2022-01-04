#!/usr/bin/python3
from botbase import *

def cloppenburg(sheets):
    data2 = get_json("https://services7.arcgis.com/sXBigjYDpL5H6l6s/arcgis/rest/services/datensammlung_shape/FeatureServer/0/query?where=1=1&outFields=*&returnGeometry=false&orderByFields=FID+desc&resultRecordCount=1&f=json")
    data2 = data2["features"][0]["attributes"]
    date = check_date(data2["Datum"], "Cloppenburg")
    data = get_json("https://services7.arcgis.com/sXBigjYDpL5H6l6s/arcgis/rest/services/LK_Gemeindegrenzen/FeatureServer/0/query?f=json&outFields=*&outStatistics=[{%22onStatisticField%22%3A%22Infektione%22%2C%22outStatisticFieldName%22%3A%22Infektione%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22gesund%22%2C%22outStatisticFieldName%22%3A%22gesund%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22die%22%2C%22outStatisticFieldName%22%3A%22die%22%2C%22statisticType%22%3A%22sum%22}]&groupByFieldsForStatistics=Stand&returnGeometry=false&where=1%3D1")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Stand"], "Cloppenburg")
    a, d, g = data["Infektione"], data["die"], data["gesund"]
    c = a + d + g
    #print(c, a,d,g)
    #for k,v in data2.items(): print(k,v,sep="\t")
    c2, cc2, g2, gg2 = data2["Inf_gesamt"], data2["neuinfekti"], data2["Genesen"], data2["neu_genesen"]
    a2, q = data2["Inf_akut"], data2["Quarantaene"]
    d2 = c2 - g2 - a2
    q = q + a
    #print(c, a,d,g,cc,gg,q)
    update(sheets, 3453, c=c, cc=cc2, g=g, gg=gg2, d=d, q=q, sig="Bot", comment="Bot Dashboard ohne SI", date=date, ignore_delta=True)
    return True

schedule.append(Task(12, 35, 19, 30, 360, cloppenburg, 3453))
if __name__ == '__main__': cloppenburg(googlesheets())
