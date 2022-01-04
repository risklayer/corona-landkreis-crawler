#!/usr/bin/python3
## Tommy
from botbase import *

_altenkirchen_c = re.compile(r"Zahl der seit Mitte März 2020 kreisweit Infizierten: ([0-9.]+)")
_altenkirchen_cc = re.compile(r"Das sind ([0-9.]+|\w+) mehr als am")
_altenkirchen_d = re.compile(r"Verstorbene: ([0-9.]+)")
_altenkirchen_g = re.compile(r"Geheilte: ([0-9.]+)")
_altenkirchen_s = re.compile(r"in stationärer Behandlung: ([0-9.]+)")

def altenkirchen(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.kreis-altenkirchen.de/INTERNET/Quicknavigation/Startseite-Kreis-Altenkirchen/-CORONA-PANDEMIE-AKTUELLES-AUS-DEM-KREIS-.php?object=tx,2154.7&ModID=7&FID=2333.4911.1&NavID=2154.2&NavID=2154.12")

    for p in soup.findAll("p"):
        if "Corona-Pandemie am" in p.text:
            content = p.get_text(strip=True, separator='\n')
            break
    #print(content)

    content_split = content.splitlines()
    ok = False
    for j in range(len(content_split)):
        if "Die Corona-Statistik für den Kreis Altenkirchen" in content_split[j]:
            date_text = content_split[j-1]
            if not today().strftime("%d. %b.") in date_text: raise NotYetAvailableException("Altenkirchen noch alt:" + date_text)
            ok = True
            break
    if not ok: raise NotYetAvailableException("Altenkirchen noch alt")

    c = force_int(_altenkirchen_c.search(content).group(1))
    cc = force_int(_altenkirchen_cc.search(content).group(1))
    d = force_int(_altenkirchen_d.search(content).group(1))
    g = force_int(_altenkirchen_g.search(content).group(1))
    s = force_int(_altenkirchen_s.search(content).group(1))

    update(sheets, 7132, c=c, cc=cc, d=d, g=g, s=s, sig="Bot")
    return True

schedule.append(Task(14, 30, 16, 30, 360, altenkirchen, 7132))
if __name__ == '__main__': altenkirchen(googlesheets())
