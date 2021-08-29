#!/usr/bin/python3
from botbase import *

def sigmaringen(sheets):
    data = get_json('https://services1.arcgis.com/e7l8Y32XFZQbVW4p/arcgis/rest/services/Coronastatistik_Extern/FeatureServer/1/query?f=json&resultRecordCount=1&where=1%3D1&orderByFields=STAND+desc&outFields=*&returnGeometry=false')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["STAND"], "Sigmaringen")
    date = data["STAND_TEXT"].replace(" - "," ").replace(" Uhr","")
    c, cc = data["ANZ_INF"], data["ANZ_INF_TAG"]
    d, dd = data["ANZ_TOD"], data["DIFF_TOD_VORTAG"]
    g, gg = data["ANZ_AQ"], data["DIFF_GEN_VORTAG"]
    update(sheets, 8437, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date)
    return True

schedule.append(Task(15, 25, 16, 10, 300, sigmaringen, 8437))
if __name__ == '__main__': sigmaringen(googlesheets())
