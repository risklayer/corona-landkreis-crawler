#!/usr/bin/python3
## Tommy
from botbase import *

_sholzland_c = re.compile(r"Die Gesamtzahl\s(?:[a-zA-ZäöüÄÖÜß]*\s)*damit\s(?:auf|bei)\s([0-9.]+)")
_sholzland_cc = re.compile(r"([0-9.]+|\w+)\s(?:neue Corona-Fälle gemeldet|COVID 19-Fälle gemeldet)")
_sholzland_date = re.compile(r"Aktuelle Info vom (\d+\.\d+\.20\d\d)")

def sholzland(sheets):
    soup = get_soup("https://www.saaleholzlandkreis.de/corona-virus/aktuelle-infos/")
    content = soup.find(id="c7419").get_text()
    date = _sholzland_date.search(content).group(1)
    check_date(date, "Saale-Holzland")
    c = force_int(_sholzland_c.search(content).group(1))
    cc = force_int(_sholzland_cc.search(content).group(1))
    update(sheets, 16074, c=c, cc=cc, sig="Bot")
    return True

schedule.append(Task(11, 11, 13, 11, 360, sholzland, 16074))
if __name__ == '__main__': sholzland(googlesheets())
