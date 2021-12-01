#!/usr/bin/python3
## Tommy

from botbase import *

_harz_cc = re.compile(r"([0-9. ]+|\w+) bestätigten? Neuinfektionen")
_harz_c = re.compile(r"seit Ausbruch der Pandemie insgesamt ([0-9. ]+)Personen positiv")
_harz_a = re.compile(r"Aktuell gibt es ([0-9. ]+|\w+) Fälle an COVID-19-Erkrankungen")
_harz_q = re.compile(r"([0-9. ]+|\w+) Personen in Quarantäne")
_harz_s = re.compile(r"([0-9.]+|\w+) COVID-19-Patienten versorgt")
_harz_i = re.compile(r"([0-9.]+|\w+) intensivmedizinisch")

def harz(sheets):

    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    domain = "https://www.kreis-hz.de/"
    soup = get_soup("https://www.kreis-hz.de/de/aktuelle-informationen-1584944219.html")

    for h3 in soup.find_all("h3"):
        header = h3.text
        if "Coronavirus" in header and "Stand vom" in header:
            if not today().strftime("%e. %B %Y") in header: raise NotYetAvailableException("Harz noch alt:" + header)
            link = h3.find_all("a", "href"==True)[1]["href"]
            break

    content = get_soup(domain+link).find("div", {"class": "gcarticle-detail-content"}).text

    c = force_int(_harz_c.search(content).group(1))
    cc = force_int(_harz_cc.search(content).group(1))

    a = force_int(_harz_a.search(content).group(1))
    temp = force_int(_harz_q.search(content).group(1))
    q = a + temp

    s = force_int(_harz_s.search(content).group(1))
    i = force_int(_harz_i.search(content).group(1))

    update(sheets, 15085, c=c, cc=cc, d=d, q=q, s=s, i=i, sig="Bot")
    return True

schedule.append(Task(11, 52, 13, 52, 360, harz, 15085))
if __name__ == '__main__': harz(googlesheets())
