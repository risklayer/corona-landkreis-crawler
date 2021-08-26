#!/usr/bin/python3
from botbase import *

def nienburg(sheets):
    data = get_json("https://services2.arcgis.com/7wuv6DH7DYhDuwvU/arcgis/rest/services/Corona_Export_gdb/FeatureServer/0/query?where=Reihenfolge%3D0&outFields=*&returnGeometry=false&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    ags, date = 3256, data["Letzte_Aktualisierung_text"]
    if not todaystr in date: raise Exception("Nienburg noch alt")
    c, cc = data["Faelle_bestaetigt"], data["Delta_Faelle_bestaetigt"]
    d, dd = data["Todesfaelle"], data["Delta_Todesfaelle"]
    g, gg = data["Faelle_genesen"], data["Delta_Faelle_genesen"]
    q = data["Aktive_Quarantaene_angeordnet"]
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, sig="Bot", date=date)
    return True

schedule.append(Task(16, 15, 18, 30, 300, nienburg, 3256))
if __name__ == '__main__': nienburg(googlesheets())
