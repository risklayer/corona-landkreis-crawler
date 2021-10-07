#!/usr/bin/python3
from botbase import *

_neumuenster_c = re.compile(r"([0-9.]+)\s+bestätigte")
_neumuenster_d = re.compile(r"([0-9.]+)\s+(?:Menschen|Personen)[^0-9]*Covid-19 verstorben", re.U)
_neumuenster_g = re.compile(r"([0-9.]+)\s+Patienten[^0-9]*Covid-19 genesen", re.U)
_neumuenster_s = re.compile(r"([0-9.]+)\s+Person(?:en)?[^0-9]*Covid-19 im Krankenhaus", re.U)
_neumuenster_q = re.compile(r"([0-9.]+)\s+Personen in Quarantäne")

def neumuenster(sheets):
    from urllib.parse import urljoin
    soup = get_soup("https://www.neumuenster.de/aktuelle-meldungen/")
    art = next(x for x in soup.find("main").findAll("article") if "Corona-Neuinfektionen" in x.get_text())
    url = urljoin("https://www.neumuenster.de/", art.find("a")["href"])
    print("Getting", url)
    soup = get_soup(url)
    main = soup.find("article")
    check_date(main.find("time")["datetime"], "Neumünster")
    text = "\n".join([x.get_text() for x in main.findAll("li")])
    #print(text)
    c = force_int(_neumuenster_c.search(text).group(1))
    d = force_int(_neumuenster_d.search(text).group(1))
    g = force_int(_neumuenster_g.search(text).group(1))
    s = force_int(_neumuenster_s.search(text).group(1))
    q = force_int(_neumuenster_q.search(text).group(1))
    update(sheets, 1004, c=c, d=d, g=g, s=s, q=q, sig="Bot")
    return True

schedule.append(Task(13, 0, 14, 35, 600, neumuenster, 1004))
if __name__ == '__main__': neumuenster(googlesheets())
