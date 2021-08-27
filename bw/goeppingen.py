#!/usr/bin/python3
from botbase import *

def goeppingen(sheets):
    import datetime, dateutil.parser
    data = get_json("https://services2.arcgis.com/NnzYQCJaH5AXJ1MQ/arcgis/rest/services/Fallzahlen_Entwicklung/FeatureServer/0/query?where=Fall_kum>0&outFields=*&orderByFields=IT+DESC&resultRecordCount=1&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    ags, date = 8117, data["Datum"]
    if not datetime.date.today().strftime("%d.%m") in date: raise Exception("Göppingen noch alt: "+str(date))
    c, cc = data["Fall_kum"], data["Neuinfi"]
    d, dd = data["Ster_kum"], data["Ster_dif"]
    g, gg = data["Gene_kum"], data["Gene_Dif"]
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date)
    return True

schedule.append(Task(13, 00, 15, 30, 360, goeppingen, 8117))
if __name__ == '__main__': goeppingen(googlesheets())
