#!/usr/bin/python3
from botbase import *

_stand = re.compile(r"Stand:")
_osterholz_c = re.compile(r"([0-9.]+) \(±?([+-]?[0-9.]+)\) Personen haben sich bisher infi?ziert", re.U)
_osterholz_g = re.compile(r"([0-9.]+) \(±?([+-]?[0-9.]+)\) Personen sind wieder genesen", re.U)
_osterholz_d = re.compile(r"([0-9.]+) \(±?([+-]?[0-9.]+)\) Personen sind verstorben", re.U)
_osterholz_q = re.compile(r"([0-9.]+) \(±?([+-]?[0-9.]+)\) Kontaktpersonen in", re.U)
_osterholz_s = re.compile(r"([0-9.]+) Personen in stationärer", re.U)

def osterholz(sheets):
    soup = get_soup("https://www.landkreis-osterholz.de/portal/meldungen/aktuelle-informationen-zum-coronavirus-901005017-21000.html?vs=1")
    content = soup.find(class_="textbaustein_content")
    date = content.find(text=_stand)
    date = check_date(date.split(" ",2)[1], "Osterholz")
    text = content.get_text("\n").strip()
    #print(text)
    c, cc = map(force_int, _osterholz_c.search(text).groups())
    g, gg = map(force_int, _osterholz_g.search(text).groups())
    d, dd = map(force_int, _osterholz_d.search(text).groups())
    q, _ = map(force_int, _osterholz_q.search(text).groups())
    s = force_int(_osterholz_s.search(text).group(1))
    q += c - g - d
    update(sheets, 3356, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, q=q, s=s, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(8, 32, 14, 35, 600, osterholz, 3356))
if __name__ == '__main__': osterholz(googlesheets())
