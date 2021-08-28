#!/usr/bin/python3
from botbase import *

def paderborn(sheets):
    data = get_json("https://utility.arcgis.com/usrsvcs/servers/ea0358e5c68e43728e4ff87217f445f0/rest/services/secure/KPB_CoronaFallzahlen_Prod_Secure/FeatureServer/1/query?f=json&where=GEM_NR=-2&returnGeometry=false&outFields=*&orderByFields=DATUM%20desc&resultRecordCount=1")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    #ags, date = 5774, datetime.datetime.utcfromtimestamp(data["DATUM"]/1000)
    #if date.date() < datetime.date.today(): raise Exception("Paderborn noch alt: "+str(date))
    date = check_date(data["DATUM"], "Paderborn")
    c, cc = data["BE_AKTUINT"], force_int(data["BE_DIF1INT"])
    d, dd = data["TO_AKTUINT"], force_int(data["TO_DIF1INT"])
    g, gg = data["GE_AKTUINT"], force_int(data["GE_DIF1INT"])
    update(sheets, 5774, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", comment="Bot Dashboard ohne QSI", date=date, ignore_delta=True)
    return True

schedule.append(Task(16, 0, 18, 30, 360, paderborn, 5774))
if __name__ == '__main__': paderborn(googlesheets())
