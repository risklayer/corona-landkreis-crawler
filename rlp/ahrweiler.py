#!/usr/bin/python3
from botbase import *

_ahrweiler_c = re.compile(r"([0-9.]+)\s+Personen mit nachgewiesen")
_ahrweiler_d = re.compile(r"([0-9.]+)\s+Personen sind an den Folgen")
_ahrweiler_g = re.compile(r"([0-9.]+)\s+Personen inzwischen wieder als genesen")

def ahrweiler(sheets):
    soup = get_soup("https://kreis-ahrweiler.de/spezial/wichtige-informationen-zum-coronavirus/aktuelle-fallzahlen-im-landkreis-ahrweiler/")
    main = soup.find(id="postArticleHero")
    t = main.get_text(" ")
    print(t)
    inam = main.find("figure").find("img")["src"]
    if not today().strftime("%d.%m.%Y") in inam: raise NotYetAvailableException("Ahrweiler noch alt:" + inam)
    c = force_int(_ahrweiler_c.search(t).group(1))
    d = force_int(_ahrweiler_d.search(t).group(1))
    g = force_int(_ahrweiler_g.search(t).group(1))
    update(sheets, 7131, c=c, d=d, g=g, sig="Bot")
    return True

schedule.append(Task(15, 30, 17, 35, 600, ahrweiler, 7131))
if __name__ == '__main__': ahrweiler(googlesheets())
