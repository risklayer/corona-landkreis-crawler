#!/usr/bin/python3
from botbase import *

_saarpfalz_c = re.compile(r"infizierten? Personen: *([0-9.]+)")
_saarpfalz_cc = re.compile(r"Neuinfektionen: *([0-9.]+)")
_saarpfalz_a = re.compile(r"infiziert:\s*([0-9.]+)", re.U)
_saarpfalz_g = re.compile(r"Genesene: *([0-9.]+)")

def saarpfalz(sheets):
    soup = get_soup("https://www.saarpfalz-kreis.de/leben-soziales-gesundheit/gesundheit/coronavirus")
    content = soup.find(id="Item.MessagePartBody")
    text = content.get_text(" ").strip()
    #print(text)
    ps = [x.get_text(" ") for x in content.findAll("p")]
    #for p in ps: print(p)
    stand = [p for p in ps if "Stand:" in p][0]
    #print(stand, today().strftime("%-d. %B"))
    if not today().strftime("%-d. %B") in stand: raise NotYetAvailableException("Saarpfalz noch alt: "+stand)
    c = force_int(_saarpfalz_c.search(text).group(1))
    a = force_int(_saarpfalz_a.search(text).group(1))
    cc = force_int(_saarpfalz_cc.search(text).group(1))
    g = force_int(_saarpfalz_g.search(text).group(1))
    d = c - g - a
    update(sheets, 10045, c=c, cc=cc, d=d, g=g, sig="Bot", ignore_delta=False)
    return True

schedule.append(Task(14, 30, 17, 35, 600, saarpfalz, 10045))
if __name__ == '__main__': saarpfalz(googlesheets())
