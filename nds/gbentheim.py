#!/usr/bin/python3
from botbase import *

def gbentheim(sheets):
    data = get_json('https://services2.arcgis.com/Nlk3vmtQwSFflkuG/ArcGIS/rest/services/LK_Fallzahlen_Zeitverlauf_aktuelle_Faelle/FeatureServer/1/query?where=Infekt_Kommul>0&outFields=*&orderByFields=Datum+DESC&resultRecordCount=1&f=json')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Datum"], "Grafschaft Bentheim")
    c, cc, d = data["Infekt_Kommul"], data["Neuinfektionen"], data["Tode_gesamt"]
    g, q = data["genesen_gesamt"], data["Quarantaene"]
    update(sheets, 3456, c=c, cc=cc, g=g, d=d, q=q, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(10, 55, 11, 20, 360, gbentheim, 3456))
schedule.append(Task(15, 15, 17, 30, 360, gbentheim, 3456))
if __name__ == '__main__': gbentheim(googlesheets())
