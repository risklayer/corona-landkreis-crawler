#!/usr/bin/python3
from botbase import *

def hildesheim(sheets):
    data = get_json("https://services2.arcgis.com/LNckHR1mV7MCT68W/arcgis/rest/services/Stats_new/FeatureServer/0/query?where=1%3D1&outFields=*&orderByFields=stand_der_fallzahlen_vom+desc&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["stand_der_fallzahlen_vom"], "Hildesheim")
    mit = data["todesfaelle_mitCovid_verst"]
    c, cc = data["infizierte_gesamt"] + mit, data["veraend_z_vortag"]
    d = data["todesfaelle"] + mit
    g, q = data["genesene"], data["quarant"]
    update(sheets, 3254, c=c, cc=cc, g=g, d=d, q=q, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(10, 4, 17, 30, 300, hildesheim, 3254))
if __name__ == '__main__': hildesheim(googlesheets())
