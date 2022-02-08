#!/usr/bin/python3
from botbase import *

_muenster_st = re.compile(r"Aktuelle Zahlen, (\d+\. \w+), (\d\d?)\.(\d\d) Uhr")
_muenster_cc = re.compile(r"Neuinfektionen:\s*([0-9.]+)", re.U)
_muenster_c = re.compile(r"bestätigten Fälle:\s*([0-9.]+)", re.U)
_muenster_d = re.compile(r"gestorbene Personen:\s*([0-9.]+)", re.U)
_muenster_g = re.compile(r"genesenen Patienten:\s*([0-9.]+)", re.U)
_muenster_si = re.compile(r"Krankenhäusern:\s*([0-9.]+)\s*davon auf Intensiv\w*:\s*([0-9.]+)", re.U)

def muenster2(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.muenster.de/corona_statistik.html")
    main = soup.find("main")
    p = main.get_text(" ").strip()
    #print(p)
    #date = check_date(p.split(":")[0], "Münster")
    d = _muenster_st.search(p)
    date = (d.group(1)+" "+d.group(2)+":"+d.group(3)) if d else p[:40]
    date = check_date(date, "Münster")
    c = force_int(_muenster_c.search(p).group(1))
    cc = force_int(_muenster_cc.search(p).group(1))
    g = force_int(_muenster_g.search(p).group(1))
    d = force_int(_muenster_d.search(p).group(1))
    s, i = map(force_int, _muenster_si.search(p).groups())
    update(sheets, 5515, c=c, cc=cc, d=d, g=g, s=s, i=i, date=date, ignore_delta="mon")
    return True

schedule.append(Task(11, 30, 13, 45, 300, muenster2, 5515))
if __name__ == '__main__': muenster2(googlesheets())
