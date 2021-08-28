#!/usr/bin/python3
from botbase import *

def hoexter(sheets):
    data = get_json("https://utility.arcgis.com/usrsvcs/servers/5ac5a1989a8a4acca85306dc23c79611/rest/services/kreis/kreis_corona_extern/MapServer/67/query?f=json&outFields=*&outStatistics=[{%22onStatisticField%22%3A%22bestaetigte_Faelle%22%2C%22outStatisticFieldName%22%3A%22bestaetigte_Faelle%22%2C%22statisticType%22%3A%22sum%22},{%22onStatisticField%22%3A%22davon_genesen%22%2C%22outStatisticFieldName%22%3A%22davon_genesen%22%2C%22statisticType%22%3A%22sum%22},{%22onStatisticField%22%3A%22oder_verstorben%22%2C%22outStatisticFieldName%22%3A%22oder_verstorben%22%2C%22statisticType%22%3A%22sum%22},{%22onStatisticField%22%3A%22stand_vom%22%2C%22outStatisticFieldName%22%3A%22stand_vom%22%2C%22statisticType%22%3A%22max%22}]&returnGeometry=false&where=1%3D1")
    data = data["features"][0]["attributes"]
    date = check_date(data["stand_vom"], "Höxter")
    data2 = get_json("https://utility.arcgis.com/usrsvcs/servers/5ac5a1989a8a4acca85306dc23c79611/rest/services/kreis/kreis_corona_extern/MapServer/68/query?f=json&outFields=*&outStatistics=[{%22onStatisticField%22%3A%22bestaetigte_Faelle%22%2C%22outStatisticFieldName%22%3A%22bestaetigte_Faelle%22%2C%22statisticType%22%3A%22sum%22},{%22onStatisticField%22%3A%22davon_genesen%22%2C%22outStatisticFieldName%22%3A%22davon_genesen%22%2C%22statisticType%22%3A%22sum%22},{%22onStatisticField%22%3A%22oder_verstorben%22%2C%22outStatisticFieldName%22%3A%22oder_verstorben%22%2C%22statisticType%22%3A%22sum%22},{%22onStatisticField%22%3A%22stand_vom%22%2C%22outStatisticFieldName%22%3A%22stand_vom%22%2C%22statisticType%22%3A%22max%22}]&returnGeometry=false&where=1%3D1")
    data2 = data2["features"][0]["attributes"]
    # for k,v in data.items(): print(k,v,sep="\t")
    #ags, date = 5762, dateutil.parser.parse(data["stand_vom"])
    #if date.date() < datetime.date.today(): raise Exception("Höxter noch alt: "+date)
    #date = date.strftime("%d.%m.%Y %H:%M")
    c, g, d = data["bestaetigte_Faelle"], data["davon_genesen"], data["oder_verstorben"]
    cc, gg, dd = data2["bestaetigte_Faelle"], data2["davon_genesen"], data2["oder_verstorben"]
    cc, gg, dd = c - cc, g - gg, dd - d
    update(sheets, 5762, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(9, 0, 10, 30, 360, hoexter, 5762))
if __name__ == '__main__': hoexter(googlesheets())
