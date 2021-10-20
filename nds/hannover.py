#!/usr/bin/python3
from botbase import *

def hannover(sheets):
    data = get_json("https://utility.arcgis.com/usrsvcs/servers/c2b4352308cb4f6d802f4e9ed0768d71/rest/services/RH_Internet/RH_COVID19_Dashboard/MapServer/3/query?f=json&cacheHint=true&outFields=*&returnGeometry=false&spatialRel=esriSpatialRelIntersects&where=1%3D1")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = data["DATUM"]
    if not today().strftime("%d.%m.%Y") in date: raise NotYetAvailableException("Hannover noch alt")
    c, cc, d, g = data["GESAMTZAHL"], data["NEUINFEKTIONEN"], data["TODESFAELLE"], data["GENESEN"]
    d += 66
    update(sheets, 3241, c=c, cc=cc, g=g, d=d, sig="Bot", comment="Bot Dashboard", date=date, ignore_delta=True)
    return True

schedule.append(Task(11, 55, 14, 30, 300, hannover, 3241))
if __name__ == '__main__': hannover(googlesheets())
