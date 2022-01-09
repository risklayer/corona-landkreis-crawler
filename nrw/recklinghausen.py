#!/usr/bin/python3
## Tommy
from botbase import *

_recklinghausen_date = re.compile(r"Stand\s(\d\d?\.\d\d?\.20\d\d)")
_recklinghausen_c = re.compile(r"([0-9.]+)\sbestätigte\sCorona-Fälle")
_recklinghausen_g = re.compile(r"([0-9.]+)\sGenesene")
_recklinghausen_d = re.compile(r"([0-9.]+)\sTodes")

def recklinghausen(sheets):
    soup = get_soup("https://www.kreis-re.de/dok/geoatlas/FME/CoStat/RepGesKra.html")
    content = soup.get_text()
    date_text = _recklinghausen_date.search(content).group(1)
    check_date(date_text, "Recklinghausen")
    c = force_int(_recklinghausen_c.search(content).group(1))
    d = force_int(_recklinghausen_d.search(content).group(1))
    g = force_int(_recklinghausen_g.search(content).group(1))
    update(sheets, 5562, c=c, d=d, g=g, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(7, 15, 9, 15, 360, recklinghausen, 5562))
if __name__ == '__main__': recklinghausen(googlesheets())
