#!/usr/bin/python3
from botbase import *

_eichsfeld_c = re.compile(r"Gesamtzahl der Infizierten: *([0-9.]+)")
_eichsfeld_cc = re.compile(r"Neuinfektionen[^:]*: *([0-9.]+)")
_eichsfeld_d = re.compile(r"Verstorbene: *[0-9.]+\** */ *([0-9.]+)")
_eichsfeld_s = re.compile(r"stationär: *([0-9.]+)")
_eichsfeld_i = re.compile(r"schwere Verläufe: *([0-9.]+)")
_eichsfeld_st = re.compile(r"Stand:\s*(\d+\.\d+\.20\d\d)", re.U)

def eichsfeld(sheets):
    soup = get_soup("https://www.kreis-eic.de/aktuelle-fallzahlen-im-landkreis-eichsfeld.html")
    article = soup.find("main").find(class_="mod_article")
    text = article.get_text()
    #print(text)
    date = check_date(_eichsfeld_st.search(text).group(1), "Eichsfeld")
    c = force_int(_eichsfeld_c.search(text).group(1))
    cc = force_int(_eichsfeld_cc.search(text).group(1))
    d = force_int(_eichsfeld_d.search(text).group(1))
    s = force_int(_eichsfeld_s.search(text).group(1))
    i = force_int(_eichsfeld_i.search(text).group(1))
    update(sheets, 16061, c=c, cc=cc, d=d, s=s, i=i, sig="Bot", date=date)
    return True

schedule.append(Task(10, 30, 12, 35, 360, eichsfeld, 16061))
if __name__ == '__main__': eichsfeld(googlesheets())
