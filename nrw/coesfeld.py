#!/usr/bin/python3
from botbase import *

def coesfeld(sheets):
    data = get_json("https://services.arcgis.com/0EDx2Zp3hlT2xyF5/ArcGIS/rest/services/Fallzahlen_Covid19_COE_sicht/FeatureServer/0/query?where=Kommune%3D%27Kreis+Coesfeld%27&outFields=*&orderByFields=datum+desc&resultRecordCount=1&f=json")
    data = data["features"][0]["attributes"]
    # for k,v in data.items(): print(k,v,sep="\t")
    ags, date = 5558, data["Stand"]
    if not todaystr in date: raise Exception("Coesfeld noch alt: "+date)
    c, cc = data["infiziert"], data["infiziert_Änderung"]
    d, dd = data["verstorben"], data["verstorben_Änderung"]
    g, gg = data["gesundet"], data["gesundet_Änderung"]
    d, g = d + 4, g - 4 # 4 "mit" Korrigieren
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(11, 30, 13, 30, 180, coesfeld, 5558))
if __name__ == '__main__': coesfeld(googlesheets())
