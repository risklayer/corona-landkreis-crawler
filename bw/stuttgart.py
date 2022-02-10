#!/usr/bin/python3
## Tommy
from botbase import *

_stuttgart_date = re.compile(r"Kennzahlen\svom\s(\d\d?\.\d\d?\.20\d\d)")
_stuttgart_c = re.compile(r"([0-9.]+)\sPersonen seit Anfang März 2020")
_stuttgart_cc = re.compile(r"März 2020 insgesamt \((?:plus|\+) ([0-9.]+) gegenüber Vortag\)")
_stuttgart_d = re.compile(r"([0-9.]+)\sPersonen\ssind\sbisher\smit\soder\san")
_stuttgart_dd = re.compile(r"verstorben\s\((?:plus|\+)\s?([0-9.]+|\w+)\sgegenüber\sVortag\).")

def stuttgart(sheets):
    soup = get_soup("https://www.stuttgart.de/leben/gesundheit/corona/fallzahlen-und-impfungen.php")
    content = soup.get_text()
    #print(content)
    date = _stuttgart_date.search(content).group(1)
    check_date(date, "Stuttgart")
    c = force_int(_stuttgart_c.search(content).group(1))
    cc = force_int(_stuttgart_cc.search(content).group(1))
    d = force_int(_stuttgart_d.search(content).group(1))
    dd = _stuttgart_dd.search(content)
    dd = force_int(dd.group(1)) if dd else None
    c += 103
    update(sheets, 8111, c=c, cc=cc, d=d, dd=dd, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(13, 35, 15, 35, 360, stuttgart, 8111))
if __name__ == '__main__': stuttgart(googlesheets())


