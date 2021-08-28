#!/usr/bin/python3
from botbase import *

def dortmund(sheets):
    data = get_csv("https://rathaus.dortmund.de/statData/shiny/FB53-Coronafallzahlen.csv")
    # print(data.tail(), data.columns)
    data2 = data.iloc[-2]
    data = data.iloc[-1]
    date = data["Datum"]
    if not todaystr in date: raise Exception("Dortmund noch alt: "+date)
    c, cc = data["positive Testergebnisse insgesamt"], data["Zuwachs positiver Testergebnisse zum Vortag"]
    d = data["Verstorben ursächlich an COVID-19"] + data["Verstorben aufgrund anderer Ursachen"]
    dd = d - (data2["Verstorben ursächlich an COVID-19"] + data2["Verstorben aufgrund anderer Ursachen"])
    g = data["genesene Personen gesamt"]
    gg = g - data2["genesene Personen gesamt"]
    s = data["darunter aktuell stationär behandelte Personen"]
    i = data["darunter aktuell intensivmedizinisch behandelte Personen"]
    ags = 5913
    update(sheets, ags, c=c, cc=cc, g=g, d=d, s=s, i=i, sig="Bot", date=date, ignore_delta=False)
    return True

schedule.append(Task(17, 00, 18, 30, 360, dortmund, 5913))
if __name__ == '__main__': dortmund(googlesheets())
