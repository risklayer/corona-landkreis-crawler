#!/usr/bin/python3
from botbase import *

def tuttlingen(sheets):
    import datetime
    data = get_json('https://services1.arcgis.com/4mOKc71W3OxwDeIs/arcgis/rest/services/Corona_Dashboard/FeatureServer/0/query?f=json&resultRecordCount=1&where=1%3D1&orderByFields=OBJECTID%20asc&outFields=*&returnGeometry=false')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    ags, date = 8327, datetime.datetime.utcfromtimestamp(data["AKTUALISIERT"]/1000)
    if date.date() < datetime.date.today(): raise Exception("Tuttlingen noch alt: "+str(date))
    date = date.strftime("%d.%m.%Y")
    c, cc = data["LKTUT_B"], data["LKTUT_B_VOR"]
    d, dd = data["LKTUT_T"], data["LKTUT_T_VOR"]
    g, gg = data["LKTUT_G"], data["LKTUT_G_VOR"]
    # TODO: IMpfungen auch?
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date)
    return True

schedule.append(Task(12, 30, 13, 30, 360, tuttlingen, 8327))
if __name__ == '__main__': tuttlingen(googlesheets())
