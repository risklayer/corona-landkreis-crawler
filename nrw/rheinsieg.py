#!/usr/bin/python3
from botbase import *

def rheinsieg(sheets):
    data = get_json("https://services3.arcgis.com/83sMx9VznDQWxJwO/arcgis/rest/services/Dashboard_Daten/FeatureServer/0/query?where=1%3D1&resultType=standard&outFields=*&orderByFields=Datum+desc&resultRecordCount=1&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Datum"], "Rhein-Sieg")
    c, cc = data["RSK"], data["RSK_Tag"]
    d = data["Verstorben"]
    g, gg = data["Geheilt"], data["Geheilt_Tag"]
    q = data["Absonderung"]
    update(sheets, 5382, c=c, cc=cc, g=g, gg=gg, d=d, q=q, sig="Bot", comment="Bot Dashboard", date=date, ignore_delta=today().weekday()==0)
    return True

schedule.append(Task(15, 30, 18, 30, 300, rheinsieg, 5382))
if __name__ == '__main__': rheinsieg(googlesheets())
