#!/usr/bin/python3
from botbase import *

_kleve_c = re.compile(r"insgesamt ([0-9.]+) bestätigte Corona-Infektionen")
_kleve_cc = re.compile(r"([0-9.]+) neue Infektionen")
_kleve_d = re.compile(r"([0-9.]+) Personen sind verstorben")
_kleve_g = re.compile(r"gelten ([0-9.]+) als genesen")
_kleve_s = re.compile(r"([0-9.]+) Personen im Krankenhaus")
_kleve_q = re.compile(r"([0-9.]+) Personen in häuslicher Quarantäne")

def kleve(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.kreis-kleve.de/de/fachbereich5/corona-virus-daten-und-fakten-pressemitteilungen/")
    main = soup.find(id="content")
    text = main.get_text(" ").strip()
    #print(text)
    if not today().strftime("%d. %B %Y, meldet") in text: raise NotYetAvailableException("Kleve noch alt:" + text[:50])
    c = force_int(_kleve_c.search(text).group(1))
    cc = force_int(_kleve_cc.search(text).group(1))
    d = force_int(_kleve_d.search(text).group(1))
    g = force_int(_kleve_g.search(text).group(1))
    s = force_int(_kleve_s.search(text).group(1))
    q = force_int(_kleve_q.search(text).group(1))
    update(sheets, 5154, c=c, cc=cc, d=d, g=g, q=q, s=s, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(12, 0, 15, 35, 600, kleve, 5154))
if __name__ == '__main__': kleve(googlesheets())
