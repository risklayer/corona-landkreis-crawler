#!/usr/bin/python3
from botbase import *

def osnabrueck(sheets):
    data = get_json("https://geo.osnabrueck.de/arcgis/rest/services/corona_lk_os_aktuellinfizierte/MapServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*")
    data = data["features"]
    #for k,v in data[0]["attributes"].items(): print(k,v,sep="\t")
    date = check_date(data[0]["attributes"]["Stand_Datum"], "Osnabrück")
    ac, ad, ag, aq = 0, 0, 0, 0,
    for rec in data:
        rec = rec["attributes"]
        if rec["GEM"] == 3404000: # STADT
            c, d = int(rec["bestaetigt"]), int(rec["Tote"])
            g, q = int(rec["Genesene"]), int(rec["Quarantaene"])
            a = c - d - g
            update(sheets, 3404, c=c, g=g, d=d, q=q+a, sig="Bot", comment="Bot API", date=date)
            continue
        ac += int(rec["bestaetigt"])
        ad += int(rec["Tote"])
        ag += int(rec["Genesene"])
        aq += int(rec["Quarantaene"])
    # Landkreis
    aa = ac - ad - ag
    update(sheets, 3459, c=ac, g=ag, d=ad, q=aq+aa, sig="Bot", comment="Bot API", date=date)
    return True

schedule.append(Task(9, 00, 11, 30, 360, osnabrueck, 3459))
if __name__ == '__main__': osnabrueck(googlesheets())
