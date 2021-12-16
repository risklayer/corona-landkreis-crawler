#!/usr/bin/python3
from botbase import *

_twonums = re.compile(r"\+?(-?\d+)\s*\(\+?\s*(-?\d+)\)")

def cottbus(sheets):
    soup = get_soup("http://www.cottbus.de/verwaltung/gb_iii/gesundheit/corona/index.html")
    main = soup.find(id="cbf_main")
    cap = main.find("caption").text
    if not today().strftime("%d.%m.%Y") in cap: raise NotYetAvailableException("Cottbus noch alt:" + cap)
    c, cc, d, dd = None, None, None, None
    s1, i1, s2, i2 = None, None, 0, 0
    for row in main.findAll("tr"):
        row = [x.text.strip() for x in row.findAll("td")]
        #print(row, _twonums.search(row[1]), force_int(row[1]))
        if len(row) != 2: continue
        if "bestätigt" in row[0]: c = force_int(row[1])
        if "zum Vortag" in row[0] and not "Verstorbene" in row[0]: cc = force_int(row[1])
        if "Verstorbene" in row[0]: d, dd = map(force_int, _twonums.search(row[1]).groups())
        if "Covid-Patienten im Carl-Thiem-Klinikum" in row[0]: s1, i1 = map(force_int, _twonums.search(row[1]).groups())
        if "Covid-Patienten im Sana-Herzzentrum" in row[0]: s2, i2 = map(force_int, _twonums.search(row[1]).groups())
    s = s1 + s2 if s1 else None
    i = i1 + i2 if i1 else None
    update(sheets, 12052, c=c, cc=cc, d=d, dd=dd, s=s, i=i, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(9, 2, 15, 35, 600, cottbus, 12052))
if __name__ == '__main__': cottbus(googlesheets())
