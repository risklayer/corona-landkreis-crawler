#!/usr/bin/python3
from botbase import *

def coesfeld(sheets):
    data = get_json("https://services.arcgis.com/0EDx2Zp3hlT2xyF5/ArcGIS/rest/services/Fallzahlen_Covid19_COE_sicht/FeatureServer/0/query?where=Kommune%3D'Kreis+Coesfeld'&outFields=*&orderByFields=datum+desc&resultRecordCount=1&f=json")
    #print(data)
    data = data["features"][0]["attributes"]
    for k,v in data.items(): print(k,v,sep="\t")
    date = data["Stand"]
    if not today().strftime("%d.%m.%Y") in date: raise NotYetAvailableException("Coesfeld noch alt: "+date)
    c, cc = data["infiziert"], data["infiziert_Änderung"]
    d, dd = data["verstorben"], data["verstorben_Änderung"]
    g, gg = data["gesundet"], data["gesundet_Änderung"]
    d, g = d + 4, g - 4 # 4 "mit" Korrigieren
    update(sheets, 5558, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(9, 30, 13, 30, 360, coesfeld, 5558))
if __name__ == '__main__': coesfeld(googlesheets())
