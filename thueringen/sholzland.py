#!/usr/bin/python3
## Tommy
from botbase import *

_sholzland_c = re.compile(r"Die Gesamtzahl\s(?:[a-zA-ZäöüÄÖÜß]*\s)*damit\s(?:auf|bei)\s([0-9.]+)")
_sholzland_cc = re.compile(r"([0-9.]+|\w+)\s(?:neue )?(Corona-Fälle|COVID 19-Fälle) gemeldet")
_sholzland_s = re.compile(r"(\d+) der Erkrankten in stationärer Behandlung")
_sholzland_i = re.compile(r"(\d+) auf Intensivstationen")
_sholzland_date = re.compile(r"Aktuelle Info vom (\d+\.\d+\.20\d\d)")

def sholzland(sheets):
    soup = get_soup("https://www.saaleholzlandkreis.de/corona-virus/aktuelle-infos/")
    cont = soup.find(id="c7419").get_text()
    for content in re.split("\n\s*\n", cont):
        date = _sholzland_date.search(content)
        c = force_int(_sholzland_c.search(content).group(1)) if _sholzland_c.search(content) else None
        cc = force_int(_sholzland_cc.search(content).group(1)) if _sholzland_cc.search(content) else None
        s = force_int(_sholzland_s.search(content).group(1)) if _sholzland_s.search(content) else None
        i = force_int(_sholzland_i.search(content).group(1)) if _sholzland_i.search(content) else None
        if date is None or c is None: continue
        #print(content)
        check_date(date.group(1), "Saale-Holzland")
        update(sheets, 16074, c=c, cc=cc, s=s, i=i)
        return True
    return False

schedule.append(Task(9, 31, 13, 11, 600, sholzland, 16074))
if __name__ == '__main__': sholzland(googlesheets())
