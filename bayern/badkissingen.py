#!/usr/bin/python3
from botbase import *

_badkissingen_c = re.compile(r"insgesamt ([0-9.]+) Corona-Fälle")
_badkissingen_c2 = re.compile(r"Gesamtinfizierten: ([0-9.]+)")
_badkissingen_cc = re.compile(r"(-?[0-9.]+) neue Corona-Fälle")
_badkissingen_cc2 = re.compile(r"Neuinfizierten: (-?[0-9.]+)")
_badkissingen_a = re.compile(r"aktuell Infizierten: (-?[0-9.]+)")
_badkissingen_d = re.compile(r"([0-9.]+) Personen, die positiv auf COVID-19 getestet waren, sind verstorben")
_badkissingen_d2 = re.compile(r"Zahl der Todesfälle im Zusammenhang mit Covid-19:? (?:\w+\s+)*([0-9.]+)[\s.]", re.U)
_badkissingen_g = re.compile(r"gesundet gelten inzwischen ([0-9.]+) Personen")
_badkissingen_s = re.compile(r"davon\swerden\s([0-9.]+)\s(?:Personen\s)?station")
_badkissingen_q = re.compile(r"([0-9.]+) Kontaktpersonen")

def badkissingen(sheets):
    soup = get_soup("https://www.landkreis-badkissingen.de/buerger--politik/aktuelle-meldungen/informationen-zum-corona-virus/10681.Aktuelle-Meldungen-zum-Coronavirus.html")
    main = soup.find("article") #.find(class_="article-detail")
    text = main.get_text(" ").strip()
    text = re.sub(r"\s+", " ", text)
    #print(text, today().strftime("am %d.%m.%Y"))
    if not today().strftime("am %d.%m.%Y") in text: raise NotYetAvailableException("Bad Kissingen noch alt: "+text[:40])
    c = force_int((_badkissingen_c.search(text) or _badkissingen_c2.search(text)).group(1))
    cc = force_int((_badkissingen_cc.search(text) or _badkissingen_cc2.search(text)).group(1))
    d = force_int((_badkissingen_d.search(text) or _badkissingen_d2.search(text)).group(1))
    m = _badkissingen_g.search(text)
    g = force_int(m.group(1)) if m else None
    m = _badkissingen_a.search(text)
    if m and not g: g = c - d - force_int(m.group(1))
    m = _badkissingen_s.search(text)
    s = force_int(m.group(1)) if m else None
    m = _badkissingen_q.search(text)
    q = force_int(m.group(1)) + c - d -g if m else None
    comment = "Bot" + (" ohne S" if s is None else "") + (" ohne Q" if q is None else "")
    update(sheets, 9672, c=c, cc=cc, d=d, g=g, q=q, s=s, sig="Bot", comment=comment, ignore_delta=True) #"mon")
    return True

schedule.append(Task(12, 2, 14, 35, 600, badkissingen, 9672))
if __name__ == '__main__': badkissingen(googlesheets())
