#!/usr/bin/python3
from botbase import *

def rheinkneuss(sheets):
    data = get_json('https://opendata.rhein-kreis-neuss.de/api/records/1.0/search/?rows=2&sort=datum&start=0&fields=datum,bestatigte_falle,infizierte,genesene,verstorben,quarantane,bestatigte_falle_vom_vortag,infizierte_im_krankenhaus,erstimpfung_personen,zweitimpfung_personen&dataset=rhein-kreis-neuss-corona-pressebericht&timezone=Europe%2FBerlin&lang=de')
    #date = check_date(data["records"][0]["record_timestamp"], "Rheinkreis Neuss")
    data1, data2 = data["records"][0]["fields"], data["records"][1]["fields"]
    date = check_date(data1["datum"], "Rheinkreis Neuss")
    #for k,v in data1.items(): print(k,v,sep="\t")
    c, cc = data1["bestatigte_falle"], data2["bestatigte_falle"]
    d, dd = data1["verstorben"], data2["verstorben"]
    g, gg = data1["genesene"], data2["genesene"]
    q, s = data1["quarantane"], data1["infizierte_im_krankenhaus"]
    # TODO: Impfungen auch?
    cc, dd, gg = c - cc, d - dd, g - gg
    q += c - d - g
    update(sheets, 5162, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, s=s, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(15, 00, 18, 00, 360, rheinkneuss, 5162))
if __name__ == '__main__': rheinkneuss(googlesheets())
