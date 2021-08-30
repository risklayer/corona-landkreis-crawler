#!/usr/bin/python3
from botbase import *

def dresden(sheets):
    data = get_json("https://services.arcgis.com/ORpvigFPJUhb8RDF/arcgis/rest/services/corona_DD_7_Sicht/FeatureServer/0/query?where=1%3D1&outFields=*&orderByFields=Datum_neu+DESC&resultRecordCount=1&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Datum_neu"], "Dresden")
    c, cc = data["Fallzahl"], data["Zuwachs_Fallzahl"]
    d, dd = data["Sterbefall"], data["Zuwachs_Sterbefall"]
    g, gg = data["Genesungsfall"], data["Zuwachs_Genesung"]
    update(sheets, 14612, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=today().weekday()==0)
    return True

schedule.append(Task(12, 5, 12, 45, 180, dresden, 14612))
schedule.append(Task(13, 0, 15, 0, 3000, dresden, 14612))
if __name__ == '__main__': dresden(googlesheets())
