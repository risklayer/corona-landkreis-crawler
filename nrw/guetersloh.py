#!/usr/bin/python3
from botbase import *

def guetersloh(sheets):
    data = get_json("https://webgis.kreis-guetersloh.de/gis/service/ags-relay/agskreisgt/guest/arcgis/rest/services/gesundheit/CoronaFallzahlen_Inzidenzen/MapServer/1/query?f=json&where=ort%3D%27Kreis%20gesamt%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=tag_id%20desc&outSR=102100&resultOffset=0&resultRecordCount=1")
    data = data["features"][0]["attributes"]
    #for k, v in data.items(): print(k, v, sep="\t")
    date = data["datum"]
    if not today().strftime("%d.%m") in date: raise NotYetAvailableException("Gütersloh noch nicht aktuell: "+date)
    c, g, d = data["summe_bestaetigt"], data["summe_genesen"], data["summe_tote"]
    aa, gg, dd = data["entwicklung_aktiv_vortag"], data["entwicklung_genesen_vortag"], data["entwicklung_tote_vortag"]
    cc = aa + gg + dd
    # TODO: Impfzahlen auch im Dashboard
    update(sheets, 5754, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", comment="Bot Dashboard ohne SI", date=date)
    return True

schedule.append(Task(10, 15, 15, 10, 360, guetersloh, 5754))
if __name__ == '__main__': guetersloh(googlesheets())
