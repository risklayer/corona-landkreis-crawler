#!/usr/bin/python3
from botbase import *

def dortmund(sheets):
    data = get_csv("https://rathaus.dortmund.de/statData/shiny/FB53-Coronafallzahlen.csv")
    #print(data.tail(), data.columns)
    data2 = data.iloc[-2]
    data = data.iloc[-1]
    date = check_date(data["Datum"], "Dortmund", datetime.timedelta(1)) + datetime.timedelta(1)
    c, cc = int(data["positive Testergebnisse insgesamt"]), int(data["Zuwachs positiver Testergebnisse zum Vortag"])
    d = int(data["Verstorben ursächlich an COVID-19"] + data["Verstorben aufgrund anderer Ursachen"])
    dd = d - int(data2["Verstorben ursächlich an COVID-19"] + data2["Verstorben aufgrund anderer Ursachen"])
    g = int(data["genesene Personen gesamt"])
    gg = int(g - data2["genesene Personen gesamt"])
    s = int(data["darunter aktuell stationär behandelte Personen"])
    i = int(data["darunter aktuell intensivmedizinisch behandelte Personen"])
    update(sheets, 5913, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, s=s, i=i, sig="Bot", comment="Bot ohne Q", date=date, ignore_delta=False)
    return True

schedule.append(Task(11, 00, 18, 30, 360, dortmund, 5913))
if __name__ == '__main__': dortmund(googlesheets())
