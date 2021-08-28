#!/usr/bin/python3
from botbase import *

def bodensee(sheets):
    data = get_json('https://services3.arcgis.com/23E2aUPiEN4SKSFV/arcgis/rest/services/Statistik_Corona_HP_allg/FeatureServer/0/query?where=1%3D1&outFields=*&orderByFields=Datum+DESC&resultRecordCount=1&f=json')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    #ags, date = 8435, datetime.datetime.utcfromtimestamp(data["Datum"]/1000)
    date = check_date(data["Datum"], "Bodensee")
    #if date.date() < datetime.date.today(): raise Exception("Bodensee noch alt: "+str(date))
    #date = date.strftime("%d.%m.%Y")
    c, cc = data["Infektionen_BSK"], data["Vortag_I"]
    d, dd = data["Todesfaelle_BSK"], data["Vortag_T"]
    g, gg = data["Genesene_BSK"], data["Vortag_G"]
    q = data["Quarant_akt"]
    # SI laden
    data = get_json('https://services3.arcgis.com/23E2aUPiEN4SKSFV/arcgis/rest/services/Statistik_Corona_HP_KKHS/FeatureServer/0/query?where=1%3D1&outFields=*&orderByFields=Datum+desc&resultRecordCount=1&f=json')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    s, i = data["COVID_19_Stationaer"], data["Intensiv_Behandelte"]
    # TODO: Impfungen auch?
    update(sheets, 8435, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, s=s, i=i, sig="", comment="C Land noch Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(16, 30, 18, 30, 360, bodensee, 8435))
if __name__ == '__main__': bodensee(googlesheets())
