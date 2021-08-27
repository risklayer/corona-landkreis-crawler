#!/usr/bin/python3
from botbase import *

def gbentheim(sheets):
    import datetime
    data = get_json('https://services2.arcgis.com/Nlk3vmtQwSFflkuG/ArcGIS/rest/services/LK_Fallzahlen_Zeitverlauf_aktuelle_Faelle/FeatureServer/1/query?where=Infekt_Kommul>0&outFields=*&orderByFields=Datum+DESC&resultRecordCount=1&f=json')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    ags, date = 3456, datetime.datetime.fromtimestamp(data["Datum"]/1000)
    if date.date() < datetime.date.today(): raise Exception("Grafschaft Bentheim noch alt")
    date = date.strftime("%d.%m.%Y %H:%M")
    c, cc, d = data["Infekt_Kommul"], data["Neuinfektionen"], data["Tode_gesamt"]
    g, q = data["genesen_gesamt"], data["Quarantaene"]
    update(sheets, ags, c=c, cc=cc, g=g, d=d, q=q, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(15, 15, 17, 30, 360, gbentheim, 3456))
if __name__ == '__main__': gbentheim(googlesheets())
