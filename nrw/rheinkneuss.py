#!/usr/bin/python3
from botbase import *

def rheinkneuss(sheets):
    data = get_json('https://opendata.rhein-kreis-neuss.de/api/records/1.0/search/?rows=2&sort=datum&start=0&fields=datum,bestatigte_falle,infizierte,genesene,verstorbene,quarantane,bestatigte_falle_vom_vortag,infizierte_im_krankenhaus,erstimpfung_personen,zweitimpfung_personen&dataset=rhein-kreis-neuss-corona-pressebericht&timezone=Europe%2FBerlin&lang=de')
    #ags, date = 5162, dateutil.parser.parse(data["records"][0]["record_timestamp"])
    date = check_date(data["records"][0]["record_timestamp"], "Rheinkreis Neuss")
    data1, data2 = data["records"][0]["fields"], data["records"][1]["fields"]
    #for k,v in data1.items(): print(k,v,sep="\t")
    #if date.date() < datetime.date.today(): raise Exception("Rheinkreis Neuss noch alt: "+str(date))
    #date = date.strftime("%d.%m.%Y %H:%M")
    c, cc = data1["bestatigte_falle"], data2["bestatigte_falle"]
    d, dd = data1["verstorbene"], data2["verstorbene"]
    g, gg = data1["genesene"], data2["genesene"]
    q, s = data1["quarantane"], data1["infizierte_im_krankenhaus"]
    # TODO: Impfungen auch?
    cc, dd, gg = c - cc, d - dd, g - gg
    update(sheets, 5162, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, s=s, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(15, 00, 18, 00, 360, rheinkneuss, 5162))
if __name__ == '__main__': rheinkneuss(googlesheets())
