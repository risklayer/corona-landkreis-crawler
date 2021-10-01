#!/usr/bin/python3
from botbase import *

_oberhausen_c = re.compile(r"seit Ausbruch: ([0-9.]+) \(([0-9.]+)\)")
_oberhausen_d = re.compile(r"Todesfälle: ([0-9.]+) \(([0-9.]+)\)")
_oberhausen_g = re.compile(r"Genesene Personen: ([0-9.]+) \(([0-9.]+)\)")
_oberhausen_q = re.compile(r"Quarantäne: ([0-9.]+) \(([0-9.]+)\)")
_oberhausen_s = re.compile(r"Krankenhaus: ([0-9.]+) \(([0-9.]+)\)")
_oberhausen_i = re.compile(r"([0-9.]+) \(\s*([0-9.]+)\s*\) Personen auf der Intensiv")

def oberhausen(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    import bs4
    soup = get_soup("https://www.oberhausen.de/de/index/rathaus/verwaltung/umwelt-gesundheit-und-mobilitat/gesundheit/aktuelle_informationen/informationen_zum_coronavirus/aktuelle_meldungen.php")
    main = soup.find(id="content")
    text = ""
    cur = next(main.find("hr").parent.children)
    while cur is not None:
        if isinstance(cur, bs4.Tag): text = text + "\n" + cur.get_text(" ")
        cur = cur.next_sibling
        if isinstance(cur, bs4.Tag) and cur.name == "hr":
            if "Aktuelle Informationen" in text: break
            text = ""
    text = text.strip()
    #print(text)
    #print(today().strftime("%-d. %B %Y"))
    if not today().strftime("%-d. %B %Y") in text: raise NotYetAvailableException("Oberhausen noch alt: "+text.split("\n")[0])
    c, cc = map(force_int, _oberhausen_c.search(text).groups())
    d, dd = map(force_int, _oberhausen_d.search(text).groups())
    g, gg = map(force_int, _oberhausen_g.search(text).groups())
    q = force_int(_oberhausen_q.search(text).group(1))
    s = force_int(_oberhausen_s.search(text).group(1))
    i = force_int(_oberhausen_i.search(text).group(1))
    cc, dd, gg = c - cc, d - dd, g - gg
    update(sheets, 5119, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, q=q, s=s, i=i, sig="Bot")
    return True

schedule.append(Task(10, 30, 12, 35, 600, oberhausen, 5119))
if __name__ == '__main__': oberhausen(googlesheets())
