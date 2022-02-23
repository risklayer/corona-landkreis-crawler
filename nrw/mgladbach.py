#!/usr/bin/python3
from botbase import *

_mgladbach_c = re.compile(r"wurde das Virus bei ([0-9.]+) (?:\(Vortag: ([0-9.]+)\))?")
_mgladbach_g = re.compile(r"sind ([0-9.]+) (?:\(Vortag: ([0-9.]+)\) )?Personen nicht mehr")
_mgladbach_a = re.compile(r"Aktuell verzeichnet das Gesundheitsamt der Stadt Mönchengladbach ([0-9.]+) (?:\(Vortag: ([0-9.]+)\) )?Personen")
_mgladbach_q = re.compile(r"befinden sich ([0-9.]+) (?:\(Vortag: ([0-9.]+)\) )?Personen in Quarantäne")
_mgladbach_d = re.compile(r"verstorbene Personen: ([0-9.]+)")
_mgladbach_i = re.compile(r"([0-9.]+) Covid-19 Fälle intensivmedizinisch")

def mgladbach(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://notfallmg.de/de/")
    main = next(x for x in soup.find(class_="main").findAll(class_="panel") if "Statusbericht" in x.get_text())
    text = main.get_text(" ").strip()
    #print(text)
    if not today().strftime("%-d. %B %Y") in text: raise NotYetAvailableException("Mönchengladbach noch alt:" + text.split("\n")[0])
    c, cc = map(force_int, _mgladbach_c.search(text).groups())
    a, aa = map(force_int, _mgladbach_a.search(text).groups())
    g, gg = None, None #map(force_int, _mgladbach_g.search(text).groups())
    q, i = None, None
    try:
        q, _ = map(force_int, _mgladbach_q.search(text).groups())
    except AttributeError: pass
    try:
        i = force_int(_mgladbach_i.search(text).group(1))
    except AttributeError: pass
    d = force_int(_mgladbach_d.search(text).group(1))
    cc, gg = c - cc if cc else None, g - gg if gg else None
    g = c - d - a if g is None and a is not None else None
    update(sheets, 5116, c=c, cc=cc, g=g, gg=gg, d=d, q=q, i=i, sig="Bot", ignore_delta=datetime.date.today().weekday()==6) # Sonntags delta ignorieren
    return True

schedule.append(Task(10, 0, 12, 35, 600, mgladbach, 5116))
if __name__ == '__main__': mgladbach(googlesheets())
