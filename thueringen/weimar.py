#!/usr/bin/python3
from botbase import *

_weimar_c = re.compile(r"positiv\s*Getesteten:\s*([0-9.]+)\s*\(Veränderung\s+zum\s*(?:Vor|Frei)tag:\s*\+?(-?[0-9.]+)", re.U)
_weimar_g = re.compile(r"Genesenen:\s*([0-9.]+)\s*\(\+?(-?[0-9.]+)\)", re.U)
_weimar_d = re.compile(r"Verstorbenen:\s*([0-9.]+)\s*\(\+?(-?[0-9.]+)\)", re.U)
_weimar_s = re.compile(r"Behandelten:\s*([0-9.]+)\s*\(\+?(-?[0-9.]+)\)", re.U)
_weimar_q = re.compile(r"Quarantäne:\s*([0-9.]+)\s*\(\+?(-?[0-9.]+)\)", re.U)
_weimar_st = re.compile(r"Stand:? *(\d\d?\.\d\d?.20\d\d(?:, \d\d?:\d\d)?)")

def weimar(sheets):
    soup = get_soup("https://stadt.weimar.de/aktuell/coronavirus/")
    article = soup.find("h3").parent
    text = article.get_text("").strip()
    date = _weimar_st.search(text)
    #print(text, date)
    date = check_date(date.group(1) if date else text[:50], "Weimar")
    c, cc = map(force_int, _weimar_c.search(text).groups())
    d, dd = map(force_int, _weimar_d.search(text).groups())
    g, gg = map(force_int, _weimar_g.search(text).groups())
    s = force_int(_weimar_s.search(text).group(1))
    q, qq = map(force_int, _weimar_q.search(text).groups())
    update(sheets, 16055, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, q=q, s=s, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(10, 00, 16, 45, 360, weimar, 16055))
if __name__ == '__main__': weimar(googlesheets())
