#!/usr/bin/python3
from botbase import *

_werrameissner_cgd = re.compile(r"([0-9.]+) Gesamtfälle, (?:[0-9.]+) Erkrankte, ([0-9.]+) Genesene, ([0-9.]+) Verstorbene")
_werrameissner_cccd = re.compile(r"([0-9.]+) neue F\wlle, ([0-9.]+) Gesamtfälle, ([0-9.]+) Verstorbene")
_werrameissner_cc = re.compile(r"([0-9.]+) neuen? Corona-F\wll")
_werrameissner_q = re.compile(r"([0-9.]+) Personen in Quarantäne")
_werrameissner_si = re.compile(r"([0-9.]+|\w+) Patienten auf der Normalstation und ([0-9.]+|\w+) Patienten (?:\([^)]*\) )?auf der Intensiv")

def werrameissner(sheets):
    soup = get_soup("https://www.werra-meissner-kreis.de/fachbereiche-einrichtungen/stab-verwaltungsleitung-und-steuerung/presse-und-oeffentlichkeitsarbeit-buergerreferat-kultur-und-kreisarchiv/presse-und-oeffentlichkeitsarbeit/pressemitteilungen")
    li = next(x for x in soup.find(id="maincontent").findAll(itemtype="http://schema.org/Article") if "Gesamtfälle" in x.get_text())
    isrc = li.find("img")["src"]
    if not today().strftime("%y.%m.%d") in isrc and not today().strftime("%d.%m.%y") in isrc: raise NotYetAvailableException("Werra-Meissner: "+isrc)
    link = li.find(href=True)["href"] if li else None
    from urllib.parse import urljoin
    link = urljoin("https://www.werra-meissner-kreis.de/fachbereiche-einrichtungen/stab-verwaltungsleitung-und-steuerung/presse-und-oeffentlichkeitsarbeit-buergerreferat-kultur-und-kreisarchiv/presse-und-oeffentlichkeitsarbeit/pressemitteilungen", link)
    print("Getting", link)
    soup = get_soup(link)
    main = soup.find(id="maincontent").find(itemtype="http://schema.org/Article")
    #check_date(li.find("time").get_text(), "Werra-Meissner")
    text = main.get_text(" ").strip()
    #print(text)
    c, g, d = map(force_int, _werrameissner_cgd.search(text).groups()) if _werrameissner_cgd.search(text) else (None, None, None)
    cc = force_int(_werrameissner_cc.search(text).group(1))
    cc, c, d = map(force_int, _werrameissner_cccd.search(text).groups()) if _werrameissner_cccd.search(text) else (cc, c, d)
    q = force_int(_werrameissner_q.search(text).group(1))
    s, i = map(force_int, _werrameissner_si.search(text).groups())
    s += i
    update(sheets, 6636, c=c, cc=cc, d=d, g=g, q=q, s=s, i=i, comment="Bot")
    return True

schedule.append(Task(10, 7, 13, 35, 600, werrameissner, 6636))
if __name__ == '__main__': werrameissner(googlesheets())
