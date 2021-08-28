
#!/usr/bin/python3
from botbase import *

def minden(sheets):
    data = get_json('https://services6.arcgis.com/Br7szJz7MbZdUpDg/arcgis/rest/services/2_Gemeinden_Corona/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&orderByFields=Datum+DESC&groupByFieldsForStatistics=Datum&outStatistics=[{%22onStatisticField%22%3A%22Absolut%22%2C%22outStatisticFieldName%22%3A%22Absolut%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22Abs_Vortag%22%2C%22outStatisticFieldName%22%3A%22Abs_Vortag%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22Tote%22%2C%22outStatisticFieldName%22%3A%22Tote%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22Tote_Vortag%22%2C%22outStatisticFieldName%22%3A%22Tote_Vortag%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22Genesen%22%2C%22outStatisticFieldName%22%3A%22Genesen%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22Gen_Vortag%22%2C%22outStatisticFieldName%22%3A%22Gen_Vortag%22%2C%22statisticType%22%3A%22sum%22}]&resultRecordCount=1&f=json')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    #ags, date = 5770, datetime.datetime.utcfromtimestamp(data["Datum"] / 1000)
    #if date.date() < datetime.date.today(): raise Exception("Minden noch alt: "+str(date))
    #date = date.strftime("%d.%m.%Y")
    date = check_date(data["Datum"], "Minden")
    c, cc = data["Absolut"], data["Abs_Vortag"]
    d, dd = data["Tote"], data["Tote_Vortag"]
    g, gg = data["Genesen"], data["Gen_Vortag"]
    cc, dd, gg = c - cc, d - dd, g - gg
    update(sheets, 5770, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", comment="Bot Dashboard", date=date, ignore_delta=True)
    return True

schedule.append(Task(16, 10, 18, 30, 360, minden, 5770))
if __name__ == '__main__': minden(googlesheets())
