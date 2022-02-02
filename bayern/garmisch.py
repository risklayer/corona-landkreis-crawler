#!/usr/bin/python3
from botbase import *

_garmisch_c = re.compile(r"([0-9.]+)\s*positiv")
_garmisch_g = re.compile(r"([0-9.]+)\s*Personen\s+sind\s+genesen")
_garmisch_d = re.compile(r"bedauern wir *([0-9.]+) *\(?intern")
_garmisch_s = re.compile(r"Hospitalisierte Personen: *([0-9.]+)")
_garmisch_i = re.compile(r"Intensiv behandelte Personen: *([0-9.]+)")

def garmisch(sheets):
    soup = get_soup("https://www.lra-gap.de/de/corona-fallzahlen-und-impf-fortschritt.html")
    main = soup.find(class_="content")
    content = main.get_text(" ").strip()
    #print(content)
    h2 = next(x for x in content.split("\n") if "Stand" in x)
    if not today().strftime("%d.%m.%Y") in h2: raise NotYetAvailableException("Garmisch noch alt: " + h2)
    c = force_int(_garmisch_c.search(content).group(1))
    d = force_int(_garmisch_d.search(content).group(1))
    g = force_int(_garmisch_g.search(content).group(1))
    s = force_int(_garmisch_s.search(content).group(1))
    i = force_int(_garmisch_i.search(content).group(1))
    update(sheets, 9180, c=c, g=g, d=d, s=s, i=i, sig="Bot")
    return True

schedule.append(Task(15, 7, 19, 35, 360, garmisch, 9180))
if __name__ == '__main__': garmisch(googlesheets())
