#!/usr/bin/python3
## Tommy
from botbase import *

_herne_c = re.compile(r"([0-9.]+) Personen eine Infektion mit Covid-19 nachgewiesen")
_herne_d = re.compile(r"([0-9.]+) Hernerinnen und Herner im Zusammenhang mit Covid-19 gestorben")
_herne_a = re.compile(r"Aktuell infiziert sind ([0-9.]+)")
_herne_s = re.compile(r"([0-9.]+) Personen stationär")

def herne(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.herne.de/Stadt-und-Leben/Gesundheit/Informationen-zum-Coronavirus/Entwicklung-in-Herne/")
    header = next(x for x in soup.find_all("h3") if "Update" in x.get_text() and "Covid" in x.get_text())
    if not today().strftime("%d. %B %Y") in header.get_text(): raise NotYetAvailableException("Herne noch alt: " + header.get_text())
    text = header.findNext("p").get_text()
    c = force_int(_herne_c.search(text).group(1))
    d = force_int(_herne_d.search(text).group(1))
    a = force_int(_herne_a.search(text).group(1))
    s = force_int(_herne_s.search(text).group(1))
    g = c - d - a
    update(sheets, 5916, c=c, d=d, g=g, s=s, sig="Bot")
    return True

schedule.append(Task(10, 15, 17, 45, 600, herne, 5916))
if __name__ == '__main__': herne(googlesheets())
