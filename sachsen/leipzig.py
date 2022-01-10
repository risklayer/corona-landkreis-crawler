#!/usr/bin/python3
## Tommy
from botbase import *

_leipzig_date = re.compile(r"Die Aktualisierung der Zahlen auf dieser Seite erfolgt Montag bis Freitag, außer an Feiertagen.\sStand\s(\d\d?\.\d\d?\.20\d\d)")
_leipzig_c = re.compile(r"positiv Getestete:\sbisher insgesamt ([0-9.]+) seit 06\.03\.2020 \(\+([0-9.]+) zum Vortag")
_leipzig_d = re.compile(r"Todesfälle:\sbisher\s([0-9.]+)\s\(\+([0-9.]+)\szum Vortag")
_leipzig_a = re.compile(r"aktive Fälle:\s([0-9.]+)")
_leipzig_q = re.compile(r"in häuslicher Quarantäne\s\(inklusive Kontaktpersonen\):\s([0-9.]+)")
_leipzig_s = re.compile(r"Patienten in Leipziger Krankenhäusern\s\(aus Stadt Leipzig und Umland\):\s([0-9.]+)")
_leipzig_i = re.compile(r"Intensivstation:\s([0-9.]+)")

def leipzig(sheets):
    soup = get_soup("https://www.leipzig.de/jugend-familie-und-soziales/gesundheit/neuartiges-coronavirus-2019-n-cov/")
    content = soup.get_text()
    date_text = _leipzig_date.search(content).group(1)
    check_date(date_text, "Leipzig")
    c, cc = map(force_int, _leipzig_c.search(content).groups())
    d, dd = map(force_int, _leipzig_d.search(content).groups())
    a = force_int(_leipzig_a.search(content).group(1))
    q = force_int(_leipzig_q.search(content).group(1))
    g = c - d - a
    si_text = soup.find(id="6-228168").get_text()
    s = force_int(_leipzig_s.search(si_text).group(1))
    i = force_int(_leipzig_i.search(si_text).group(1))
    update(sheets, 14713, c=c, cc=cc, d=d, dd=dd, g=g, q=q, s=s, i=i, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(8, 25, 10, 25, 360, leipzig, 14713))
if __name__ == '__main__': leipzig(googlesheets())
