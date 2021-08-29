#!/usr/bin/python3
from botbase import *

def goslar(sheets):
    data = get_json("https://services9.arcgis.com/Tjs4RI43tb8dPEcZ/arcgis/rest/services/Corona_Fallzahlen_LK_Goslar_View/FeatureServer/0/query?f=json&where=GEN%3D'Landkreis+Goslar'&outFields=*&returnGeometry=false")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Datum"], "Goslar", datetime.timedelta(days=1, hours=12))
    c, cc = int(data["Bestaetigt"]), int(data["Infektionsdelta_Vortag"])
    d, g = int(data["Verstorben"]), int(data["Genesen"])
    update(sheets, 3153, c=c, cc=cc, g=g, d=d, sig="Bot")
    return True

schedule.append(Task(11, 15, 12, 30, 360, goslar, 3153))
if __name__ == '__main__': goslar(googlesheets())
