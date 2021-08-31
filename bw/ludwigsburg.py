#!/usr/bin/python3
from botbase import *

def ludwigsburg(sheets):
    data = get_json("https://services8.arcgis.com/K8jt9QACjKo097DD/arcgis/rest/services/Corona_Dashboard_Einz/FeatureServer/0/query?where=1%3D1&outFields=*&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Datum"], "Ludwigsburg")
    c, cc = data["Best_Faelle_LGA"], data["Diff_Best_Faelle_LGA"]
    d, dd = data["Todesf_LGA"], data["Diff_Todesf_LGA"]
    g, gg = data["Genesene"], data["Diff_Genesene"]
    update(sheets, 8118, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(16, 00, 18, 30, 300, ludwigsburg, 8118))
if __name__ == '__main__': ludwigsburg(googlesheets())
