#!/usr/bin/python3
## Tommy

from botbase import *

_suhl_cc = re.compile(r"Neu gemeldete Fälle: ([0-9.]+)")
_suhl_c = re.compile(r"Fälle aufaddiert: ([0-9.]+)")
_suhl_d = re.compile(r"Verstorbene: ([0-9.]+)")
_suhl_q = re.compile(r"aktuell unter Quarantäne: ([0-9.]+)")
_suhl_st = re.compile(r"(\d\d?\.\d\d?\.20\d\d)")

def suhl(sheets):

    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.suhltrifft.de/content/blogcategory/277/2269/")

    date_line = soup.find("table", {"class": "blog"}).find_all("tr")[1].find("table")
    date = _suhl_st.search(date_line.text.strip()).group(1)
    check_date(date, "Suhl")

    content = date_line.findNext("table").text.strip()

    c = force_int(_suhl_c.search(content).group(1))
    cc = force_int(_suhl_cc.search(content).group(1))
    d = force_int(_suhl_d.search(content).group(1))
    q = force_int(_suhl_q.search(content).group(1))

    update(sheets, 16054, c=c, cc=cc, d=d, q=q, sig="Bot")
    return True

schedule.append(Task(10, 45, 12, 30, 360, suhl, 16054))
if __name__ == '__main__': suhl(googlesheets())
