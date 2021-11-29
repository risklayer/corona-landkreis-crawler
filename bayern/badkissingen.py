#!/usr/bin/python3
from botbase import *

_badkissingen_c = re.compile(r"insgesamt ([0-9.]+) Corona-Fälle")
_badkissingen_cc = re.compile(r"(-?[0-9.]+) neue Corona-Fälle")
_badkissingen_d = re.compile(r"([0-9.]+) Personen, die positiv auf COVID-19 getestet waren, sind verstorben")
_badkissingen_g = re.compile(r"gesundet gelten inzwischen ([0-9.]+) Personen")
_badkissingen_s = re.compile(r"davon werden ([0-9.]+) stationär")
_badkissingen_q = re.compile(r"([0-9.]+) Kontaktpersonen")

def badkissingen(sheets):
    soup = get_soup("https://www.landkreis-badkissingen.de/buerger--politik/aktuelle-meldungen/informationen-zum-corona-virus/10681.Aktuelle-Meldungen-zum-Coronavirus.html")
    main = soup.find("article") #.find(class_="article-detail")
    text = main.get_text(" ").strip()
    print(text)
    if not today().strftime("am %d.%m.%Y") in text: raise NotYetAvailableException("Bad Kissingen noch alt.")
    c = force_int(_badkissingen_c.search(text).group(1))
    cc = force_int(_badkissingen_cc.search(text).group(1))
    d = force_int(_badkissingen_d.search(text).group(1))
    g = force_int(_badkissingen_g.search(text).group(1))
    m = _badkissingen_s.search(text)
    s = force_int(m.group(1)) if m else None
    q = force_int(_badkissingen_q.search(text).group(1)) + c - d -g
    update(sheets, 9672, c=c, cc=cc, d=d, g=g, q=q, s=s, sig="Bot", ignore_delta=True) #"mon")
    return True

schedule.append(Task(12, 2, 14, 35, 600, badkissingen, 9672))
if __name__ == '__main__': badkissingen(googlesheets())
