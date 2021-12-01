#!/usr/bin/python3
## Tommy

from botbase import *

_saalfeld_cc = re.compile(r"([0-9.]+|\w+) neuen? Coronafälle")
_saalfeld_c = re.compile(r"infizierten Personen seit Beginn der Pandemie beträgt damit ([0-9.]+)")
_saalfeld_d = re.compile(r"([0-9.]+) Menschen im Zusammenhang mit einer")
_saalfeld_st = re.compile(r"(\d\d?\.\d\d?\.20\d\d)")

def saalfeld(sheets):

    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    domain = "https://www.kreis-slf.de"
    soup = get_soup("https://www.kreis-slf.de/landkreis/")

    for h4 in soup.find_all("h4"):
        if "neue Coronafälle" in h4.text:
            date_text = h4.findPrevious("time").text.strip()
            link = h4.findNext("div", {"class": "teaser-text"}).find("a")["href"]
            break

    date = _saalfeld_st.search(date_text).group(1)
    check_date(date, "Saalfeld")

    content = get_soup(domain+link).find("div", {"itemprop": "articleBody"}).text

    c = force_int(_saalfeld_c.search(content).group(1))
    cc = force_int(_saalfeld_cc.search(content).group(1))
    d = force_int(_saalfeld_d.search(content).group(1))

    update(sheets, 16073, c=c, cc=cc, d=d, sig="Bot")
    return True

schedule.append(Task(15, 45, 17, 45, 360, saalfeld, 16073))
if __name__ == '__main__': saalfeld(googlesheets())
