#!/usr/bin/python3
from botbase import *

_ostprignitz_c = re.compile(r"Bestätigte Fälle: *([0-9.]+), davon neu: (\d+)")
_ostprignitz_g = re.compile(r"Genesungen: *([0-9.]+)(?:, davon neu: (\d+))?")
_ostprignitz_d = re.compile(r"Sterbefälle: *([0-9.]+)")
_ostprignitz_st = re.compile(r"Stand: *(\d\d?\.\d\d?\.20\d\d), (\d\d)(?:\.(\d\d))?")

def ostprignitz(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.ostprignitz-ruppin.de/Informationen/Corona-Infos/")
    text = soup.find(class_="main-content-area").get_text(" ").strip()
    #print(text)
    date = _ostprignitz_st.search(text)
    date = date.group(1)+" "+date.group(2)+":"+(date.group(3) or "00") if date else None
    date = check_date(date, "Ostprignitz")
    c, cc = map(force_int, _ostprignitz_c.search(text).groups())
    g, gg = map(force_int, _ostprignitz_g.search(text).groups())
    d = force_int(_ostprignitz_d.search(text).group(1))
    c, g = c + 3, g + 3
    update(sheets, 12068, c=c, cc=cc, d=d, g=g, gg=gg, date=date, ignore_delta=True)
    return True

schedule.append(Task(12, 00, 17, 35, 360, ostprignitz, 12068))
if __name__ == '__main__': ostprignitz(googlesheets())
