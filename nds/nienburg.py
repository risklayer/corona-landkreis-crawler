#!/usr/bin/python3
from botbase import *

def nienburg(sheets):
    data = get_json("https://services2.arcgis.com/7wuv6DH7DYhDuwvU/arcgis/rest/services/Corona_Export_gdb/FeatureServer/0/query?where=Reihenfolge%3D0&outFields=*&returnGeometry=false&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = data["Letzte_Aktualisierung_text"].replace(",","").replace(" Uhr","")
    if not today().stftime("%d.%m.%Y") in date: raise NotYetAvailableException("Nienburg noch alt")
    c, cc = data["Faelle_bestaetigt"], data["Delta_Faelle_bestaetigt"]
    d, dd = data["Todesfaelle"], data["Delta_Todesfaelle"]
    g, gg = data["Faelle_genesen"], data["Delta_Faelle_genesen"]
    q = data["Aktive_Quarantaene_angeordnet"]
    update(sheets, 3256, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(16, 15, 20, 30, 300, nienburg, 3256))
if __name__ == '__main__': nienburg(googlesheets())
