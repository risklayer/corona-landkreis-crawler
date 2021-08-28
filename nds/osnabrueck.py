#!/usr/bin/python3
from botbase import *

def osnabrueck(sheets):
    import datetime
    data = get_json("https://geo.osnabrueck.de/arcgis/rest/services/corona_lk_os_aktuellinfizierte/MapServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*")
    data = data["features"]
    #for k,v in data[0]["attributes"].items(): print(k,v,sep="\t")
    date = datetime.datetime.utcfromtimestamp(data[0]["attributes"]["Stand_Datum"] / 1000)
    if date.date() < datetime.date.today(): raise Exception("Osnabrück noch alt: "+str(date))
    date = date.strftime("%d.%m.%Y")
    ac, ad, ag, aq = 0, 0, 0, 0,
    for rec in data:
        rec = rec["attributes"]
        if rec["GEM"] == 3404000:
            ags = 3404 # Stadt
            c, d = int(rec["bestaetigt"]), int(rec["Tote"])
            g, q = int(rec["Genesene"]), int(rec["Quarantaene"])
            update(sheets, ags, c=c, g=g, d=d, q=q, sig="Bot", comment="API", date=date)
            continue
        ac += int(rec["bestaetigt"])
        ad += int(rec["Tote"])
        ag += int(rec["Genesene"])
        aq += int(rec["Quarantaene"])
    ags = 3459 # Land
    update(sheets, ags, c=ac, g=ag, d=ad, q=aq, sig="Bot", comment="API", date=date)
    return True

schedule.append(Task(9, 00, 10, 30, 360, osnabrueck, 3459))
if __name__ == '__main__': osnabrueck(googlesheets())
