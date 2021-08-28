#!/usr/bin/python3
from botbase import *

def hildesheim(sheets):
    data = get_json("https://services2.arcgis.com/LNckHR1mV7MCT68W/arcgis/rest/services/Stats_new/FeatureServer/0/query?where=1%3D1&outFields=*&orderByFields=stand_der_fallzahlen_vom+desc&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    #ags, date = 3254, datetime.datetime.fromtimestamp(data["stand_der_fallzahlen_vom"]/1000)
    #if date.date() < datetime.date.today(): raise Exception("Hildesheim noch alt: "+str(date))
    #date = date.strftime("%d.%m.%Y %H:%M")
    date = check_date(data["stand_der_fallzahlen_vom"], "Hildesheim")
    mit = data["todesfaelle_mitCovid_verst"]
    c, cc = data["infizierte_gesamt"] + mit, data["veraend_z_vortag"]
    d = data["todesfaelle"] + mit
    g, q = data["genesene"], data["quarant"]
    update(sheets, 3254, c=c, cc=cc, g=g, d=d, q=q, sig="Bot", date=date)
    return True

schedule.append(Task(16, 00, 17, 30, 300, hildesheim, 3254))
if __name__ == '__main__': hildesheim(googlesheets())
