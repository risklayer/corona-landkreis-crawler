#!/usr/bin/python3
from botbase import *

def goeppingen(sheets):
    data = get_json("https://services2.arcgis.com/NnzYQCJaH5AXJ1MQ/arcgis/rest/services/Fallzahlen_Entwicklung_neu2/FeatureServer/0/query?where=Fall_kum>0&outFields=*&orderByFields=IT+DESC&resultRecordCount=1&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = data["Datum"]
    if not today().strftime("%d.%m") in date: raise NotYetAvailableException("Göppingen noch alt: "+str(date))
    c, cc = data["Fall_kum"], data["Neuinfi"]
    d, dd = data["Ster_kum"], data["Ster_dif"]
    g, gg = data["Gene_kum"], data["Gene_Dif"]
    update(sheets, 8117, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=today().weekday()==0)
    return True

schedule.append(Task(13, 00, 15, 30, 360, goeppingen, 8117))
if __name__ == '__main__': goeppingen(googlesheets())
