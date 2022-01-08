#!/usr/bin/python3
from botbase import *

_ffb_c = re.compile(r"Stand\s\w+,\s(\d\d?\.\d\d?.20\d\d)\s\((\d\d?:\d\d)\sUhr\),\sgibt\ses\sinsgesamt\s([0-9.]+)\sCorona-Infizierte", re.U)
_ffb_d = re.compile(r"Todesfälle insgesamt mit Covid-19-Befund und Wohnsitz im Landkreis Fürstenfeldbruck: ([0-9.]+) \(Stand (\d\d\.\d\d.20\d\d)\)")
_ffb_g = re.compile(r"Genesene: ([0-9.]+) Personen \(Stand (\d\d\.\d\d.20\d\d)\)")

def ffb(sheets):
    soup = get_soup("https://www.lra-ffb.de/aktuelles/corona-informationen/corona-statistik-infizierte-genesene-verstorbene-und-geimpfte-im-landkreis")
    text = soup.find(class_="content").get_text()
    #print(text)
    m = _ffb_c.search(text).groups()
    date = " ".join(m[0:2])
    date = check_date(date, "Fürstenfeldbruck")
    c = force_int(m[2])
    m2 = _ffb_d.search(text).groups()
    d = force_int(m2[0]) if m2[1] == m2[1] else None
    m2 = _ffb_g.search(text).groups()
    g = force_int(m2[0]) if m2[1] == m2[1] else None
    update(sheets, 9179, c=c, d=d, g=g, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(11, 0, 16, 35, 360, ffb, 9179))
if __name__ == '__main__': ffb(googlesheets())
