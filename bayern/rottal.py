#!/usr/bin/python3
## Tommy
from botbase import *

_rottal_date = re.compile(r"Stand (\d\d?\.\d\d?\.20\d\d)")
_rottal_c = re.compile(r"Indexfälle gesamt\s*([0-9.]+)")
_rottal_cc = re.compile(r"Indexfälle heute\s*([0-9.]+)")
_rottal_a = re.compile(r"Aktuell positive Fälle\s*([0-9.]+)")
_rottal_d = re.compile(r"Todesfälle gesamt\s*([0-9.]+)")
_rottal_dd = re.compile(r"Todesfälle heute\s*([0-9.]+)")
_rottal_si = re.compile(r"Indexfälle im Krankenhaus\s*\(davon auf Intensivstation\)\s*([0-9.]+)\s+\(([0-9.]+)\)")

def rottal(sheets):
    soup = get_soup("https://www.rottal-inn.de/buergerservice-formulare/gesundheitsamt/coronavirus-aktuelle-informationen/fallzahlen-und-statistiken-fuer-den-landkreis-rottal-inn/")
    header = soup.find("div", {"class": "tab-card__accordion"}).find("div", {"class": "tab__title"})
    content = header.findNext("div", {"class": "tab__content"}).get_text()
    date_text = _rottal_date.search(header.get_text()).group(1)
    date = check_date(date_text, "Rottal", datetime.timedelta(1)) + datetime.timedelta(1)
    #print(content)
    c = force_int(_rottal_c.search(content).group(1))
    cc = force_int(_rottal_cc.search(content).group(1))
    a = force_int(_rottal_a.search(content).group(1))
    d = force_int(_rottal_d.search(content).group(1))
    dd = force_int(_rottal_dd.search(content).group(1))
    s, i = map(force_int, _rottal_si.search(content).groups())
    g = c - d - a
    update(sheets, 9277, c=c, cc=cc, d=d, dd=dd, g=g, s=s, i=i, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(9, 27, 16, 48, 900, rottal, 9277))
if __name__ == '__main__': rottal(googlesheets())
