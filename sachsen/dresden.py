#!/usr/bin/python3
from botbase import *

def dresden(sheets):
    data = get_json("https://services.arcgis.com/ORpvigFPJUhb8RDF/arcgis/rest/services/corona_DD_7_Sicht/FeatureServer/0/query?where=1%3D1&outFields=*&orderByFields=Datum_neu+DESC&resultRecordCount=1&f=json")
    data = data["features"][0]["attributes"]
    # for k,v in data.items(): print(k,v,sep="\t")
    #ags, date = 14612, datetime.datetime.utcfromtimestamp(data["Datum_neu"]/1000)
    #if date.date() < datetime.date.today(): raise Exception("Dresden noch alt: "+str(date))
    #date = date.strftime("%d.%m.%Y %H:%M")
    date = check_date(data["Datum_neu"], "Dresden")
    c, cc = data["Fallzahl"], data["Zuwachs_Fallzahl"]
    d, dd = data["Sterbefall"], data["Zuwachs_Sterbefall"]
    g, gg = data["Genesungsfall"], data["Zuwachs_Genesungsfall"]
    update(sheets, 14612, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(12, 5, 12, 45, 180, dresden, 14612))
schedule.append(Task(13, 0, 15, 0, 3000, dresden, 14612))
if __name__ == '__main__': dresden(googlesheets())
