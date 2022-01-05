#!/usr/bin/python3
## Tommy

from botbase import *

_aachen_c = re.compile(r"Seit Ende Februar 2020 wurden insgesamt ([0-9.]+)")
_aachen_d = re.compile(r"Die Zahl der gemeldeten Todesfälle liegt bei ([0-9.]+)")

def aachen(sheets):

    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.aachen.de/DE/stadt_buerger/notfall_informationen/corona/aktuelles/index.html")
    header = next(p.get_text() for p in soup.find_all("p") if "Aktuelle Lage Stadt und StädteRegion Aachen zum Corona-Virus" in p.get_text())
    if not today().strftime("%e. %B %Y") in header: raise NotYetAvailableException("Aachen noch alt: " + header[24:])
    content = soup.get_text()
    c = force_int(_aachen_c.search(content).group(1))
    d = force_int(_aachen_d.search(content).group(1))

    update(sheets, 5334, c=c, d=d, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(15, 50, 17, 50, 360, aachen, 5334))
if __name__ == '__main__': aachen(googlesheets())
