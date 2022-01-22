#!/usr/bin/python3
## Tommy

from botbase import *

_harz_cc = re.compile(r"([0-9. ]+|\w+) bestätigten? Neuinfektionen")
_harz_c = re.compile(r"seit Ausbruch der Pandemie insgesamt ([0-9. ]+)Personen positiv")
_harz_a = re.compile(r"Aktuell gibt es ([0-9. ]+|\w+) Fälle an COVID-19-Erkrankungen")
_harz_q = re.compile(r"([0-9. ]+|\w+) Personen in Quarantäne")
_harz_s = re.compile(r"([0-9.]+|\w+) COVID-19-Patienten versorgt")
_harz_i = re.compile(r"([0-9.]+|\w+) intensivmedizinisch")
_harz_d = re.compile(r"Verstorbenen im Zusammenhang mit COVID-19 steigt damit auf ([0-9.]+|\w+)")

def harz(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.kreis-hz.de/de/aktuelle-informationen-1584944219.html")
    entry = next(x for x in soup.find(id="section_1_1343_1167").find_all("article") if "Coronavirus" in x.get_text() and "Stand" in x.get_text())
    link = entry.find(href=True)["href"] if entry else None
    #print(entry, link)
    if not today().strftime("%e. %B %Y") in entry.get_text(): raise NotYetAvailableException("Harz noch alt:" + entry.get_text())
    from urllib.parse import urljoin
    link = urljoin("https://www.kreis-hz.de/de/aktuelle-informationen-1584944219.html", link)
    print("Getting", link)
    content = get_soup(link).find("div", {"class": "gcarticle-detail-content"}).text

    c = force_int(_harz_c.search(content).group(1))
    cc = force_int(_harz_cc.search(content).group(1))

    a = force_int(_harz_a.search(content).group(1))
    temp = force_int(_harz_q.search(content).group(1))
    q = a + temp

    s = force_int(_harz_s.search(content).group(1)) if _harz_s.search(content) else None
    i = force_int(_harz_i.search(content).group(1)) if _harz_i.search(content) else None

    d = force_int(_harz_d.search(content).group(1)) if _harz_d.search(content) else None
    g = c - d - a if d else None

    comment = "Bot ohne DG" if d is None else "Bot"
    comment += " A"+str(a)
    update(sheets, 15085, c=c, cc=cc, d=d, g=g, q=q, s=s, i=i, sig=str(a), comment=comment, ignore_delta=True) #"mon")
    return True

schedule.append(Task(14, 52, 16, 52, 360, harz, 15085))
if __name__ == '__main__': harz(googlesheets())
