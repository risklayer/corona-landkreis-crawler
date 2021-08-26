#!/usr/bin/python3
from botbase import *

def wuppertal(sheets):
    from urllib.request import urlopen
    import json, datetime
    url = "https://services6.arcgis.com/LJkXU8kMjITiDcBM/ArcGIS/rest/services/Corona_Statistik_Presse/FeatureServer/0/query?where=1%3D1&resultType=none&returnGeodetic=false&outFields=*&returnGeometry=false&f=pjson"
    client = urlopen(url)
    data = client.read()
    client.close()
    data = json.loads(data)
    latest = data["features"][-1]["attributes"]
    #print(latest)
    date = datetime.datetime.fromtimestamp(latest["DATUM"]/1000).date()
    if date != datetime.date.today(): raise Exception("Wuppertal noch nicht aktuell")
    ags, hour = 5124, datetime.datetime.now().hour
    g, d = latest["ABGESCHL"], latest["D_TOD_SUM"]
    c = latest["INFIZIERT"] + g + d
    sig, comment = "Bot", "Bot"
    if hour < 20: sig, comment = "Vorläufig", "Zwischenstand Bot"
    date = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=hour).strftime("%d.%m.%Y %H:%M")
    update(sheets, ags, c=c, g=g, d=d, sig=sig, comment=comment, dry_run=dry_run, date=date, check=lambda x: x != None and x.startswith("Vorläufig"))
    if hour < 20: return False
    return True

schedule.append(Task(10, 5, 20, 30, 3600, wuppertal, 5124))
if __name__ == '__main__': wuppertal(googlesheets())
