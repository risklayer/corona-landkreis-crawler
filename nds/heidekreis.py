#!/usr/bin/python3
from botbase import *

def heidekreis(sheets):
    data = get_json("https://services1.arcgis.com/CSnFgu7AbHmWtZb9/arcgis/rest/services/Covid19_Entwicklung_LKHK_Public/FeatureServer/0/query?f=json&where=ver_ffentlichen_ver_ffentlichen%3D%27Ja%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=50&resultType=standard&cacheHint=true")
    data = data["features"][0]["attributes"]
    # for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["datum_ttmmjjjj"], "Heidekreis")
    c, cc = data["bisher_best_tigte_f_lle"], data["differenz_zum_vortag"]
    d, dd = data["gesamt_verstorbene"], data["differenz_zum_vortag_verstorben"]
    g, gg = data["aktuell_anzahl_genesene"], data["differenz_zum_vortag_genesene"]
    s, i = data["betreuter_personen_im_hk_klinik"], data["intensivmedizinisch_betreuter_p"]
    # TODO: Impfungen auch?
    update(sheets, 3358, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, s=s, i=i, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(12, 15, 13, 30, 180, heidekreis, 3358))
if __name__ == '__main__': heidekreis(googlesheets())
