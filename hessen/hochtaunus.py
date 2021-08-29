#!/usr/bin/python3
from botbase import *

def hochtaunus(sheets):
    data = get_json("https://services7.arcgis.com/On3dBC5z3wJpjJVV/arcgis/rest/services/Covid_Fallzahlen_aktuelles_Datum/FeatureServer/0/query?where=Gen%3D%27Hochtaunuskreis%27&outFields=*&returnGeometry=false&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Datum"], "Hochtaunuskreis")
    c, cc = data["Faelle"], data["Faelle_Delta_Vortag"]
    d, dd = data["Verstorben"], data["Verstorben_Delta_Vortag"]
    g, gg = data["Genesene"], data["Genesene_Delta_Vortag"]
    s, i = data["KKH_Pat"], data["KKH_Int"]
    # TODO: Impfungen auch?
    update(sheets, 6434, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, s=s, i=i, sig="Bot", date=date)
    return True

schedule.append(Task(16, 30, 21, 30, 600, hochtaunus, 6434))
if __name__ == '__main__': hochtaunus(googlesheets())
