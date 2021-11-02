#!/usr/bin/python3
from botbase import *

_kitzingen_c = re.compile(r"([0-9.]+) bestätigte Corona-Fälle")
_kitzingen_d = re.compile(r"([0-9.]+) Personen davon sind gestorben")
_kitzingen_g = re.compile(r"([0-9.]+) Personen gesund")
_kitzingen_q = re.compile(r"([0-9.]+) Personen sind als enge Kontaktpersonen")

def kitzingen(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    from urllib.parse import urljoin
    soup = get_soup("https://www.kitzingen.de/buergerservice/aktuelles/aktuelles-2020/uebersichtsseite-corona/")
    text = soup.find(id="maincontent").find(class_="text").get_text(" ").strip()
    text = re.sub("\s+", " ", text)
    #print(text)
    if not today().strftime("%-d. %B %Y") in text: raise NotYetAvailableException("Kitzingen: "+text[:50])
    c = force_int(_kitzingen_c.search(text).group(1))
    d = force_int(_kitzingen_d.search(text).group(1))
    g = force_int(_kitzingen_g.search(text).group(1))
    q = force_int(_kitzingen_q.search(text).group(1)) + c - d - g
    update(sheets, 9675, c=c, d=d, g=g, q=q, sig="Bot")
    return True

schedule.append(Task(10, 2, 14, 35, 600, kitzingen, 9675))
if __name__ == '__main__': kitzingen(googlesheets())
