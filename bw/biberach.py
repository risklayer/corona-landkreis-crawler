#!/usr/bin/python3
from botbase import *

def biberach(sheets):
    data = get_json('https://services9.arcgis.com/41cRQoNICXEIjSKu/arcgis/rest/services/Covid19/FeatureServer/2/query?where=1%3D1&outFields=*&returnGeometry=false&outStatistics=[{%22onStatisticField%22%3A%22Fallzahlen%22%2C%22outStatisticFieldName%22%3A%22Fallzahlen%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22Genesene%22%2C%22outStatisticFieldName%22%3A%22Genesene%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22Todesfaelle%22%2C%22outStatisticFieldName%22%3A%22Todesfaelle%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22FZ_Diff_Vortag%22%2C%22outStatisticFieldName%22%3A%22FZ_Diff_Vortag%22%2C%22statisticType%22%3A%22sum%22}%2C{"onStatisticField"%3A"Stand"%2C"outStatisticFieldName"%3A"Stand"%2C"statisticType"%3A"max"}]&f=json')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    #ags, date = 8426, dateutil.parser.parse(data["Stand"])
    date = check_date(data["Stand"], "Biberach")
    #if date.date() < datetime.date.today(): raise Exception("Biberach noch alt: "+str(date))
    #date = date.strftime("%d.%m.%Y %H:%M")
    c, cc = data["Fallzahlen"], data["FZ_Diff_Vortag"]
    d, g = data["Todesfaelle"], data["Genesene"]
    update(sheets, 8426, c=c, cc=cc, g=g, d=d, sig="Bot", comment="Bot Dashboard", date=date)
    return True

schedule.append(Task(15, 00, 16, 30, 300, biberach, 8426))
if __name__ == '__main__': biberach(googlesheets())
