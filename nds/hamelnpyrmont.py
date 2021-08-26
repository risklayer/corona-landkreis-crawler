#!/usr/bin/python3
from botbase import *

def hamelnpyrmont(sheets):
    from urllib.request import urlopen
    import json, datetime
    url = "https://services2.arcgis.com/50d5wsDbZicDslDY/ArcGIS/rest/services/Gemeinden_F_Covid/FeatureServer/0/query?where=Status%3D%27an%27&outFields=*&returnGeometry=false&orderByFields=Datum+DESC&groupByFieldsForStatistics=Datum&outStatistics=[{%22onStatisticField%22%3A%22i_gesamt%22%2C%22outStatisticFieldName%22%3A%22i_gesamt%22%2C%22statisticType%22%3A%22sum%22}%2C%0D%0A{%22onStatisticField%22%3A%22infiziert%22%2C%22outStatisticFieldName%22%3A%22infiziert%22%2C%22statisticType%22%3A%22sum%22}%2C%0D%0A{%22onStatisticField%22%3A%22genesen%22%2C%22outStatisticFieldName%22%3A%22genesen%22%2C%22statisticType%22%3A%22sum%22}%2C%0D%0A{%22onStatisticField%22%3A%22neu_infizierte_zum_Vortag%22%2C%22outStatisticFieldName%22%3A%22neu_infizierte_zum_Vortag%22%2C%22statisticType%22%3A%22sum%22}%2C{%22onStatisticField%22%3A%22Todesf%C3%A4ll%22%2C%22outStatisticFieldName%22%3A%22Todesf%C3%A4ll%22%2C%22statisticType%22%3A%22sum%22}%2C%0D%0A{%22onStatisticField%22%3A%22quarantaen%22%2C%22outStatisticFieldName%22%3A%22quarantaen%22%2C%22statisticType%22%3A%22sum%22}]&resultRecordCount=1&f=json"
    client = urlopen(url)
    data = client.read()
    client.close()
    data = json.loads(data)
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = datetime.datetime.fromtimestamp(data["Datum"]/1000)
    if date.date() < datetime.date.today(): raise Exception("Coesfeld noch alt")
    c, cc = data["i_gesamt"], data["neu_infizierte_zum_Vortag"]
    d, a, q = data["Todesfäll"], data["infiziert"], data["quarantaen"]
    c, d = c + 13, d + 3
    g = c - a - d
    ags, date = 3252, date.strftime("%d.%m.%Y %H:%M")
    update(sheets, ags, c=c, cc=cc, g=g, d=d, q=q, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(11, 55, 12, 30, 180, hamelnpyrmont, 3252))

def main():
    sheets = build('sheets', 'v4', credentials=authorize()).spreadsheets()
    hamelnpyrmont(sheets)

if __name__ == '__main__':
    main()
