#!/usr/bin/python3
from botbase import *

def ludwigsburg(sheets):
    import datetime
    data = get_json("https://services8.arcgis.com/K8jt9QACjKo097DD/arcgis/rest/services/Corona_Dashboard_Einz/FeatureServer/0/query?where=1%3D1&outFields=*&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    ags, date = 8118, datetime.datetime.fromtimestamp(data["Datum"] / 1000)
    if date.date() < datetime.date.today(): raise Exception("Ludwigsburg noch alt: "+str(date))
    date = date.strftime("%d.%m.%Y %H:%M")
    #c, cc = data["Faelle_Gesamt"], data["Diff_Faelle_Gesamt"]
    #d, dd = data["Tode_Gesamt"], data["Diff_Tode_Gesamt"]
    c, cc = data["Best_Faelle_LGA"], data["Diff_Best_Faelle_LGA"]
    d, dd = data["Todesf_LGA"], data["Diff_Todesf_LGA"]
    g, gg = data["Genesene"], data["Diff_Genesene"]
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(17, 00, 18, 30, 300, ludwigsburg, 8118))
if __name__ == '__main__': ludwigsburg(googlesheets())
