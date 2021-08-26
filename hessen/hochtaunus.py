#!/usr/bin/python3
from botbase import *

def hochtaunus(sheets):
    import datetime
    data = get_json("https://services7.arcgis.com/On3dBC5z3wJpjJVV/arcgis/rest/services/Covid_Fallzahlen_aktuelles_Datum/FeatureServer/0/query?where=Gen%3D%27Hochtaunuskreis%27&outFields=*&returnGeometry=false&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    ags, date = 6434, datetime.datetime.fromtimestamp(data["Datum"] / 1000)
    if date.date() < datetime.date.today(): raise Exception("Hochtaunuskreis noch alt: "+str(date))
    date = date.strftime("%d.%m.%Y")
    c, cc = data["Faelle"], data["Faelle_Delta_Vortag"]
    d, dd = data["Verstorben"], data["Verstorben_Delta_Vortag"]
    g, gg = data["Genesene"], data["Genesene_Delta_Vortag"]
    s, i = data["KKH_Pat"], data["KKH_Int"]
    # TODO: Impfungen auch?
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, s=s, i=i, sig="Bot", date=date)
    return True

schedule.append(Task(17, 30, 21, 30, 600, hochtaunus, 6434))
if __name__ == '__main__': hochtaunus(googlesheets())
