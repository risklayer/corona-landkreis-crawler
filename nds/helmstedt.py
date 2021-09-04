#!/usr/bin/python3
from botbase import *

def helmstedt(sheets):
    data = get_json("https://geoportal.helmstedt.de/arcgis/rest/services/Projekte/Covid19_LKHE_Werte/FeatureServer/0/query?f=json&cacheHint=true&resultOffset=0&resultRecordCount=25&where=1%3D1&outFields=*&returnGeometry=false&spatialRel=esriSpatialRelIntersects")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = data["Datum_text"]
    if not today().strftime("%d.%m.%Y") in date: raise NotYetAvailableException("Helmstedt noch alt: "+date)
    c, cc = data["bestaetigt"], data["Inf_zum_Vortag"]
    d = data["Todesfaelle"]
    g, gg = data["genesen"], data["Genesen_zum_Vortag"]
    q = data["Quarantaene"] + data["derzeit_krank"]
    # TODO: Impfungen auch?
    update(sheets, 3154, c=c, cc=cc, g=g, gg=gg, d=d, q=q, sig="Bot", date=date)
    return True

schedule.append(Task(14, 30, 17, 30, 300, helmstedt, 3154))
if __name__ == '__main__': helmstedt(googlesheets())
