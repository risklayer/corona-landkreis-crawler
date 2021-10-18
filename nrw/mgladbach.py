#!/usr/bin/python3
from botbase import *

_mgladbach_c = re.compile(r"wurde das Virus bei ([0-9.]+) \(Vortag: ([0-9.]+)\)")
_mgladbach_g = re.compile(r"sind ([0-9.]+) \(Vortag: ([0-9.]+)\) Personen nicht mehr")
_mgladbach_q = re.compile(r"befinden sich ([0-9.]+) \(Vortag: ([0-9.]+)\) Personen in Quarantäne")
_mgladbach_d = re.compile(r"verstorbene Personen: ([0-9.]+)")

def mgladbach(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://notfallmg.de/de/")
    main = soup.find(class_="main").find(class_="panel")
    text = main.get_text(" ").strip()
    #print(text)
    if not today().strftime("%-d. %B %Y") in text: raise NotYetAvailableException("Mönchengladbach noch alt:" + ps[0])
    c, cc = map(force_int, _mgladbach_c.search(text).groups())
    g, gg = map(force_int, _mgladbach_g.search(text).groups())
    q, qq = map(force_int, _mgladbach_q.search(text).groups())
    d = force_int(_mgladbach_d.search(text).group(1))
    cc, gg, qq = c - cc, g - gg, q - qq
    update(sheets, 5116, c=c, cc=cc, g=g, gg=gg, d=d, q=q, sig="Bot", ignore_delta=datetime.date.today().weekday()==6) # Sonntags delta ignorieren
    return True

schedule.append(Task(10, 0, 12, 35, 600, mgladbach, 5116))
if __name__ == '__main__': mgladbach(googlesheets())
