#!/usr/bin/python3
from botbase import *

def rheinerft(sheets):
    import datetime
    data = get_json("https://services7.arcgis.com/lDivAOFOYuYRJqnX/arcgis/rest/services/REK_C19/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&f=json")
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    ags, date = 5362, datetime.datetime.utcfromtimestamp(data["EditDate"] / 1000)
    if date.date() < datetime.date.today(): raise Exception("Rhein-Erft noch alt: "+str(date))
    date = date.strftime("%d.%m.%Y %H:%M")
    c, cc = data["IndexfaelleInsgesamt"], data["VeraenderungVortagIi"]
    d, dd = data["Todesfaelle"], data["VeraenderungVortagT"]
    g, gg = data["Genesen"], data["VeraenderungVortagG"]
    q = data["PersonenInQuarantaene"]
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, sig="Bot", comment="Dashboard ohne SI", date=date)
    return True

schedule.append(Task(16, 15, 18, 30, 300, rheinerft, 5362))
if __name__ == '__main__': rheinerft(googlesheets())
