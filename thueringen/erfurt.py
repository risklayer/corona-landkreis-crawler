#!/usr/bin/python3
from botbase import *

_erfurt_c = re.compile(r"Gesamtzahl der Infizierten: *([0-9.]+)")
_erfurt_cc = re.compile(r"Neuinfektionen \([^)]*\): *([0-9.]+)")
_erfurt_d = re.compile(r"Verstorbene: *([0-9.]+)")
_erfurt_g = re.compile(r"Genesene: *([0-9.]+)")
_erfurt_st = re.compile(r"Übermittlungsstand:\s*(\d+\.\d+\.20\d\d)", re.U)

def erfurt(sheets):
    soup = get_soup("https://www.erfurt.de/ef/de/service/aktuelles/topthemen/coronavirus/index.html")
    article = soup.find("main").find("section").find(class_="ym-gl")
    text = article.get_text()
    #print(text)
    date = check_date(_erfurt_st.search(text).group(1), "Erfurt")
    c = force_int(_erfurt_c.search(text).group(1))
    cc = force_int(_erfurt_cc.search(text).group(1))
    d = force_int(_erfurt_d.search(text).group(1))
    g = force_int(_erfurt_g.search(text).group(1))
    update(sheets, 16051, c=c, cc=cc, d=d, g=g, sig="Bot", date=date)
    return True

schedule.append(Task(8, 00, 12, 35, 360, erfurt, 16051))
if __name__ == '__main__': erfurt(googlesheets())
