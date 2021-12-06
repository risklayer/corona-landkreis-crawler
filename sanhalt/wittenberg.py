#!/usr/bin/python3
## Tommy

from botbase import *

_wittenberg_c = re.compile(r"insgesamt\s*([0-9.]+)\s*Infizierten")
_wittenberg_d = re.compile(r"([0-9.]+) Personen sind im Zusammenhang mit einer Covid-19-Infektion gestorben")
_wittenberg_cc = re.compile(r"([0-9.]+|\w+) Neuinfektionen")
_wittenberg_st = re.compile(r"Stand (\d\d?\.\d\d?\.20\d\d)")

def wittenberg(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.landkreis-wittenberg.de/de/aktuelle-informationen.html")
    header = soup.find("h3")
    content = header.findNext("p").text
    #print(content)

    date = _wittenberg_st.search(header.text).group(1)
    check_date(date, "Wittenberg")

    c = force_int(_wittenberg_c.search(content).group(1))
    cc = force_int(_wittenberg_cc.search(content).group(1))
    d = force_int(_wittenberg_d.search(content).group(1)) if _wittenberg_d.search(content) else None

    update(sheets, 15091, c=c, cc=cc, d=d, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(15, 5, 16, 35, 360, wittenberg, 15091))
if __name__ == '__main__': wittenberg(googlesheets())
