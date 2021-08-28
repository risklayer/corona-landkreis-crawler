#!/usr/bin/python3
from botbase import *

def heidelbergrnk(sheets):
    data = get_json("https://services7.arcgis.com/0Uc5jDlEgdLosloE/arcgis/rest/services/dbdata_hd_rnk03/FeatureServer/0/query?where=date%3C%3D%27"+today().strftime("%Y-%m-%d")+"%27&outFields=*&orderByFields=date+desc&resultRecordCount=1&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    #date = dateutil.parser.parse(data["date_act"]).date()
    date = check_date(data["date_act"], "Heidelberg")
    #if date < datetime.date.today(): raise Exception("Heidelberg noch alt: "+str(date))
    #date = date.strftime("%d.%m.%Y")
    # Heidelberg
    c, cc = data["ges_hd"], data["ges_dif_hd"]
    d, dd = data["vst_hd"], data["vst_dif_hd"]
    g, gg = data["gn_hd"], data["gn_dif_hd"]
    update(sheets, 8221, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date)
    # Rhein-Neckar-Kreis
    c, cc = data["ges_rnk"], data["ges_dif_rnk"]
    d, dd = data["vst_rnk"], data["vst_dif_rnk"]
    g, gg = data["gn_rnk"], data["gn_dif_rnk"]
    update(sheets, 8228, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date)
    return True

schedule.append(Task(7, 55, 9, 30, 300, heidelbergrnk, 8226))
if __name__ == '__main__': heidelbergrnk(googlesheets())
