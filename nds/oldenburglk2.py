#!/usr/bin/python3
from botbase import *

_oldenburglk_st = re.compile(r"Stand: *(\d\d?\.\d\d?\.20\d\d, \d\d?:\d\d)")
_oldenburglk_c = re.compile(r"([0-9.]+) bestätigte Fälle")
_oldenburglk_cc = re.compile(r"([0-9.]+) Neuinfektionen")
_oldenburglk_g = re.compile(r"([0-9.]+) Personen als wieder genesen")
_oldenburglk_d = re.compile(r"([0-9.]+) Personen sind verstorben")
_oldenburglk_q = re.compile(r"Quarantäne befinden sich derzeit im Kreisgebiet ([0-9.]+) Personen")

def oldenburglk2(sheets):
    soup = get_soup("https://www.oldenburg-kreis.de/portal/seiten/coronavirus-900000764-21700.html?rubrik=900000005&naviID=reset1&vs=1")
    content = soup.find(class_="innen").get_text(" ")
    #print(content)
    date = _oldenburglk_st.search(content).group(1)
    date = check_date(date, "Oldenburg")
    c = force_int(_oldenburglk_c.search(content).group(1))
    cc = force_int(_oldenburglk_cc.search(content).group(1))
    d = force_int(_oldenburglk_d.search(content).group(1))
    g = force_int(_oldenburglk_g.search(content).group(1))
    q = force_int(_oldenburglk_q.search(content).group(1))
    update(sheets, 3458, c=c, cc=cc, g=g, d=d, q=q, sig="Bot", comment="Bot Dashboard", date=date, ignore_delta=True)
    return True

schedule.append(Task(12, 25, 19, 30, 600, oldenburglk2, 3458))
if __name__ == '__main__': oldenburglk2(googlesheets())
