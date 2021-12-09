#!/usr/bin/python3
from botbase import *

_saarpfalz_c = re.compile(r"infizierten? Personen:\s*([0-9.]+)", re.U)
_saarpfalz_cc = re.compile(r"Neuinfektionen: *([0-9.]+)")
_saarpfalz_a = re.compile(r"infiziert:\s*([0-9.]+)", re.U)
_saarpfalz_g = re.compile(r"Genesene: *([0-9.]+)")
_saarpfalz_st = re.compile(r"Stand: \w+, (\d+\. \w+), \d+(?:[.:]\d\d)? Uhr")

def saarpfalz(sheets):
    soup = get_soup("https://www.saarpfalz-kreis.de/leben-soziales-gesundheit/gesundheit/coronavirus")
    content = soup.find("article").find("section")
    text = content.get_text(" ").strip()
    #print(text)
    date = _saarpfalz_st.search(text)
    date = date.group(1) if date else text[:100]
    check_date(date, "Saarpfalz")
    c = force_int(_saarpfalz_c.search(text).group(1))
    a = force_int(_saarpfalz_a.search(text).group(1)) if _saarpfalz_a.search(text) else None
    cc = force_int(_saarpfalz_cc.search(text).group(1))
    g = force_int(_saarpfalz_g.search(text).group(1)) if _saarpfalz_g.search(text) else None
    d = c - g - a if a and g else None
    com = "Bot" if d else "Bot unvollständig"
    update(sheets, 10045, c=c, cc=cc, d=d, g=g, sig="Bot", comment=com, ignore_delta="mon")
    return True

schedule.append(Task(14, 30, 17, 35, 600, saarpfalz, 10045))
if __name__ == '__main__': saarpfalz(googlesheets())
