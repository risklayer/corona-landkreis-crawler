#!/usr/bin/python3
from botbase import *

_stand = re.compile(r"Aktueller Stand Corona:?\s*\((\d{1,2}\.\d{1,2}\.20\d\d)\)")
_row_c = re.compile(r"bisher ([0-9.]+) Fälle", re.U)
_row_cc = re.compile(r"([0-9.]+) neue Corona-Fälle", re.U)
_row_g = re.compile(r"([0-9.]+) davon sind mittlerweile wieder genesen", re.U)
_row_d = re.compile(r"Verstorben \(Gesamtzahl Fälle\)\n\s*([0-9.]+) Personen", re.U | re.M)
_row_q = re.compile(r" ([0-9.]+) Kontaktpersonen in Quarantäne", re.U)
_row_s = re.compile(r"([0-9.]+|\w+) Person(?:en)? in stationärer", re.U)

def row(sheets):
    soup = get_soup("https://www.lk-row.de/portal/seiten/aktuelle-zahlen-corona--900000752-23700.html?vs=1")
    content = soup.find(id="nolis_content_site").find(class_="innen")
    text = content.get_text("\n").strip()
    #print(text)
    date = check_date(_stand.search(text).group(1), "Rotenburg-Wümme")
    c = force_int(_row_c.search(text).group(1))
    cc = force_int(_row_cc.search(text).group(1))
    d = force_int(_row_d.search(text).group(1))
    g = force_int(_row_g.search(text).group(1))
    q = force_int(_row_q.search(text).group(1))
    m = _row_s.search(text)
    s = force_int(m.group(1)) if m else None
    q += c - g - d
    update(sheets, 3357, c=c, cc=cc, d=d, g=g, q=q, s=s, sig="Bot", ignore_delta=False)
    return True

schedule.append(Task(11, 32, 16, 35, 360, row, 3357))
if __name__ == '__main__': row(googlesheets())
