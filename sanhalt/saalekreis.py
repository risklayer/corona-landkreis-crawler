#!/usr/bin/python3
from botbase import *

_saale_c = re.compile(r"bestätigte Fälle gesamt: *([0-9.]+)")
_saale_cc = re.compile(r"Neuinfektionen: *([0-9.]+)")
_saale_d = re.compile(r"verstorben: *([0-9.]+)")
_saale_g = re.compile(r"wieder gesund: *([0-9.]+)")
_saale_date = re.compile(r"Stand: *(\d+\.\d+\.20\d\d)")

def saalekreis(sheets):
    data = get_soup('https://www.saalekreis.de/de/aktuelles-corona/coronavirus-zahlen.html')
    main = data.find("article")
    text = main.get_text(" ").strip()
    #print(text)
    date = _saale_date.search(text).group(1)
    date = check_date(date, "Saalekreis")
    c = force_int(_saale_c.search(text).group(1))
    cc = force_int(_saale_cc.search(text).group(1))
    d = force_int(_saale_d.search(text).group(1))
    g = force_int(_saale_g.search(text).group(1))
    update(sheets, 15088, c=c, cc=cc, g=g, d=d, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(13, 00, 15, 30, 300, saalekreis, 15088))
if __name__ == '__main__': saalekreis(googlesheets())
