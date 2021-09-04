#!/usr/bin/python3
from botbase import *

_essen_c = re.compile(r"insgesamt ([0-9.]+) Essener")
_essen_d = re.compile(r"([0-9.]+) Essener\*innen [a-zA-Z -]+? verstorben")
_essen_g = re.compile(r"wieder genesen sind ([0-9.]+)")
_essen_s = re.compile(r"([0-9.]+) Essener\*innen stationär")
_essen_i = re.compile(r"([0-9.]+) davon intensiv")
_essen_q = re.compile(r"([0-9.]+) Essener\*innen [a-zA-Zä ]+? Quarantäne")

def essen2(sheets):
    soup = get_soup("https://www.essen.de/leben/gesundheit/corona_virus/coronavirus_updates.de.html")
    main = soup.find(id="contentMitte")
    ps = [x.parent.parent for x in main.findAll(text=re.compile(r"\d+\.\d+\.20\d\d, \d+:\d+ Uhr"))]
    p = next(p for p in ps if "Essener Coronavirus-Situation" in p.get_text())
    text = p.get_text(" ")
    #print(text)
    datestr = p.find("strong").text.rstrip(":")
    date = check_date(datestr, "Essen")
    c = force_int(_essen_c.search(text).group(1))
    d = force_int(_essen_d.search(text).group(1))
    g = force_int(_essen_g.search(text).group(1))
    s = force_int(_essen_s.search(text).group(1))
    i = force_int(_essen_i.search(text).group(1))
    q = force_int(_essen_q.search(text).group(1))
    update(sheets, 5113, c=c, g=g, d=d, q=q, s=s, i=i, sig="Bot", date=date)
    return True

schedule.append(Task(10, 30, 12, 35, 600, essen2, 5113))
if __name__ == '__main__': essen2(googlesheets())
