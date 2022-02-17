#!/usr/bin/python3
## Tommy
from botbase import *

_aachen_c = re.compile(r"Seit Ende Februar 2020 wurden beim Robert.Koch.Institut \(RKI\) insgesamt ([0-9.]+)")
_aachen_d = re.compile(r"Die Zahl der gemeldeten Todesfälle liegt bei ([0-9.]+)")
_aachen_a = re.compile(r"Aktuell sind ([0-9.]+) Menschen nachgewiesen")

def aachen(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.aachen.de/DE/stadt_buerger/notfall_informationen/corona/aktuelles/index.html")
    header = next(p.get_text() for p in soup.find_all(["p","h2"]) if "Aktuelle Lage Stadt und StädteRegion Aachen zum Corona-Virus" in p.get_text())
    if not today().strftime("%e. %B %Y") in header: raise NotYetAvailableException("Aachen noch alt: " + header[24:])
    content = soup.get_text()
    c = force_int(_aachen_c.search(content).group(1))
    d = force_int(_aachen_d.search(content).group(1))
    g = (c - d - force_int(_aachen_a.search(content).group(1))) if _aachen_a.search(content) else None
    com = "Bot ohne G" if g is None else "Bot"
    update(sheets, 5334, c=c, d=d, g=g, sig="Bot", comment=com, ignore_delta=True)
    return True

schedule.append(Task(10, 15, 17, 50, 600, aachen, 5334))
if __name__ == '__main__': aachen(googlesheets())
