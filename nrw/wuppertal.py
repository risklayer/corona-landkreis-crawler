#!/usr/bin/python3
from botbase import *

def wuppertal(sheets):
    data = get_json("https://services6.arcgis.com/LJkXU8kMjITiDcBM/ArcGIS/rest/services/Corona_Statistik_Presse/FeatureServer/0/query?where=1%3D1&resultType=none&returnGeodetic=false&outFields=*&returnGeometry=false&f=pjson")
    latest = data["features"][-1]["attributes"]
    date = check_date(latest["DATUM"], "Wuppertal")
    hour = datetime.datetime.now().hour
    g, d = latest["ABGESCHL"], latest["D_TOD_SUM"]
    c = latest["INFIZIERT"] + g + d
    sig, comment = "Bot", "Bot"
    if hour < 20: sig, comment = "Vorläufig", "Zwischenstand"
    date = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=hour) #.strftime("%d.%m.%Y %H:%M")
    update(sheets, 5124, c=c, g=g, d=d, sig=sig, comment=comment, date=date, check=lambda x: x == None or x == "" or x == "Vorläufig")
    return hour >= 20

schedule.append(Hourly(10, 5, 21, 30, 3600, wuppertal, 5124))
if __name__ == '__main__': wuppertal(googlesheets())
