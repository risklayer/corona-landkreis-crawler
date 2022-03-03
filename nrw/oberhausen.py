#!/usr/bin/python3
from botbase import *

_oberhausen_c = re.compile(r"seit Ausbruch:\s*([0-9.]+) \(([0-9.]+)\)")
_oberhausen_d = re.compile(r"Todesfälle:\s*([0-9.]+) \(([0-9.]+)\)")
_oberhausen_g = re.compile(r"Genesene Personen:\s*([0-9.]+) \(([0-9.]+)\)")
_oberhausen_q = re.compile(r"Quarantäne:\s*([0-9.]+) \(([0-9.]+)\)")
_oberhausen_s = re.compile(r"Krankenhaus:\s*([0-9.]+) \(([0-9.]+)\)")
_oberhausen_i = re.compile(r"([0-9.]+) \(\s*([0-9.]+)\s*\) Personen auf der Intensiv")

def oberhausen(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    import bs4
    soup = get_soup("https://www.oberhausen.de/de/index/rathaus/verwaltung/soziales-gesundheit-wohnen-und-recht/gesundheit/aktuelle_informationen/informationen_zum_coronavirus/aktuelle_meldungen.php")
    main = soup.find(id="content")
    text = ""
    cur = next(main.find("h2").parent.children)
    while cur is not None:
        if isinstance(cur, bs4.Tag): text = text + "\n" + cur.get_text(" ")
        cur = cur.next_sibling
        if isinstance(cur, bs4.Tag) and cur.name == "hr":
            if "Aktuelle Informationen" in text: break
            text = ""
    text = re.sub(r"\s+", " ", text.strip()) # geschützte leerzeichen...
    #print(text)
    #print(today().strftime("%A, %-d. %B %Y"))
    if not today().strftime("Aktuelle Informationen von %A, %-d. %B") in text: raise NotYetAvailableException("Oberhausen noch alt: "+text.split("\n")[0][:80])
    c, cc = map(force_int, _oberhausen_c.search(text).groups())
    d, dd = map(force_int, _oberhausen_d.search(text).groups())
    g, gg = map(force_int, _oberhausen_g.search(text).groups())
    q = force_int(_oberhausen_q.search(text).group(1)) if _oberhausen_q.search(text) else None
    s, i = None, None
    try:
        s = force_int(_oberhausen_s.search(text).group(1))
        i = force_int(_oberhausen_i.search(text).group(1))
    except: pass
    cc, dd, gg = c - cc, d - dd, g - gg
    update(sheets, 5119, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, q=q, s=s, i=i, sig="Bot")
    return True

schedule.append(Task(10, 3, 14, 35, 600, oberhausen, 5119))
if __name__ == '__main__': oberhausen(googlesheets())
