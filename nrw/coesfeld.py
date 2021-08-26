#!/usr/bin/python3
from botbase import *

def coesfeld(sheets):
    from urllib.request import urlopen
    import json, datetime
    url = "https://services.arcgis.com/0EDx2Zp3hlT2xyF5/ArcGIS/rest/services/Fallzahlen_Covid19_COE_sicht/FeatureServer/0/query?where=Kommune%3D%27Kreis+Coesfeld%27&outFields=*&orderByFields=datum+desc&resultRecordCount=1&f=json"
    client = urlopen(url)
    data = client.read()
    client.close()
    data = json.loads(data)
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = datetime.datetime.fromtimestamp(data["Datum"]/1000)
    if date.date() < datetime.date.today(): raise Exception("Coesfeld noch alt")
    c, cc = data["infiziert"], data["infiziert_Änderung"]
    d, dd = data["verstorben"], data["verstorben_Änderung"]
    g, gg = data["gesundet"], data["gesundet_Änderung"]
    c, g = c + 4, g - 4 # 4 "mit" Korrigieren
    ags, date = 5558, data["Stand"]
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", dry_run=dry_run, date=date, ignore_delta=True)
    return True

schedule.append(Task(11, 30, 13, 30, 180, coesfeld, 5558))
if __name__ == '__main__': coresfeld(googlesheets())
