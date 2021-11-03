#!/usr/bin/python3
from botbase import *

_steinburg_c = re.compile(r"([0-9.]+)\s*positiv\s+bestätigte")
_steinburg_g = re.compile(r"([0-9.]+)\s*Genesene")
_steinburg_d = re.compile(r"([0-9.]+)\s*Verstorbene")
_steinburg_q = re.compile(r"([0-9.]+)\s+begründete")
_steinburg_st = re.compile(r"Stand: (\d+\.\d+\.20\d\d)")

def steinburg(sheets):
    import bs4
    soup = get_soup("https://www.steinburg.de/startseite.html")
    main = soup.find(id="content-main-right")
    main = next(x for x in main.findAll(class_="tile-box") if "Corona-Fallzahlen" in x.get_text())
    text = main.get_text(" ").strip()
    #print(text)
    date = check_date(_steinburg_st.search(text).group(1), "Steinburg")
    c = force_int(_steinburg_c.search(text).group(1))
    g = force_int(_steinburg_g.search(text).group(1))
    d = force_int(_steinburg_d.search(text).group(1))
    q = force_int(_steinburg_q.search(text).group(1)) + c - d - g
    update(sheets, 1061, c=c, d=d, g=g, q=q, sig="Bot")
    return True

schedule.append(Task(16, 14, 19, 35, 360, steinburg, 1061))
if __name__ == '__main__': steinburg(googlesheets())
