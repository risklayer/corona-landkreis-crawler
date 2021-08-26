#!/usr/bin/python3
from botbase import *

def rheinsieg(sheets):
    import datetime
    data = get_json("https://services3.arcgis.com/83sMx9VznDQWxJwO/arcgis/rest/services/Dashboard_Daten/FeatureServer/0/query?where=1%3D1&resultType=standard&outFields=*&orderByFields=Datum+desc&resultRecordCount=1&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    ags, date = 5382, datetime.datetime.fromtimestamp(data["Datum"] / 1000)
    if date.date() < datetime.date.today(): raise Exception("Rheinsieg noch alt: "+str(date))
    date = date.strftime("%d.%m.%Y %H:%M")
    c, cc = data["RSK"], data["RSK_Tag"]
    d = data["Verstorben"]
    g, gg = data["Geheilt"], data["Geheilt_Tag"]
    q = data["Absonderung"]
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, q=q, sig="Bot", comment="Dashboard", date=date)
    return True

schedule.append(Task(16, 15, 18, 30, 300, rheinsieg, 5382))
if __name__ == '__main__': rheinsieg(googlesheets())
