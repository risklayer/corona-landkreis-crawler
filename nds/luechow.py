#!/usr/bin/python3
from botbase import *

_luechow_c = re.compile(r"([0-9.]+) *\(\+?(-?[0-9]+) Neuinfektionen\) *COVID-19-Fälle")
_luechow_a = re.compile(r"([0-9.]+) *(?:\(\+?(-?[0-9]+)\))? *aktive Fälle")
_luechow_g = re.compile(r"([0-9.]+) *Genesene")
_luechow_d = re.compile(r"([0-9.]+) *(?:\(\+?(-?[0-9]+)\))? *Verstorbene")
_luechow_q1 = re.compile(r"([0-9.]+) *(?:\(\+?(-?[0-9]+)\))? *Kontaktpersonen")
_luechow_q2 = re.compile(r"([0-9.]+) *(?:\(\+?(-?[0-9]+)\))? *Reiserückkehrer")
_luechow_s = re.compile(r"in einem Krankenhaus: ([0-9.]+)")
_luechow_st = re.compile(r"Fallzahlen\s*\(Stand:\s*(\d\d?\.\s*\w+\s+20\d\d), (\d\d?)(?:\.(\d\d))?\s*Uhr", re.M)

def luechow(sheets):
    soup = get_soup("https://www.luechow-dannenberg.de/home/familie-soziales-gesundheit/corona-virus.aspx")
    articles = soup.find(class_="DetailView-description")
    text = articles.get_text(" ").strip()
    #print(text)
    m = _luechow_st.search(text)
    date = m.group(1) + " " +m.group(2) + ":" + (m.group(3) if m.group(3) else "00")
    date = check_date(date, "Lüchow-Dannenberg")
    c, cc = map(force_int, _luechow_c.search(text).groups())
    a, aa = map(force_int, _luechow_a.search(text).groups())
    d, dd = map(force_int, _luechow_d.search(text).groups())
    q1 = force_int(_luechow_q1.search(text).group(1))
    q2 = force_int(_luechow_q2.search(text).group(1))
    s = force_int(_luechow_s.search(text).group(1))
    g = c - d - a
    q = q1 + q2 + a
    update(sheets, 3354, c=c, cc=cc, d=d, dd=dd, g=g, q=q, s=s, date=date, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(16, 30, 19, 35, 360, luechow, 3354))
if __name__ == '__main__': luechow(googlesheets())
