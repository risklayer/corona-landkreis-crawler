#!/usr/bin/python3
from botbase import *

_stormarn_c = re.compile(r"bestätigten COVID-19-Fälle von *([0-9.]+)")
_stormarn_g = re.compile(r"([0-9.]+) Personen gelten als genesen")
_stormarn_d = re.compile(r"([0-9.]+) Personen sind verstorben")

def stormarn(sheets):
    import bs4
    soup = get_soup("https://www.kreis-stormarn.de/aktuelles/pressemeldungen/2021/zahl-der-bestaetigten-corona-faelle-in-stormarn.html")
    main = soup.find("main")
    date = check_date(main.find(class_="release").get_text(), "Stormarn")
    text = ""
    cur = main.find("h4")
    while True:
        text += cur.get_text(" ").strip()+"\n"
        cur = cur.next_sibling
        if isinstance(cur, bs4.Tag) and cur.name == "h4": break
    text = text.strip()
    #print(text)
    c = force_int(_stormarn_c.search(text).group(1))
    g = force_int(_stormarn_g.search(text).group(1))
    d = force_int(_stormarn_d.search(text).group(1))
    update(sheets, 1062, c=c, d=d, g=g, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(14, 14, 19, 35, 360, stormarn, 1062))
if __name__ == '__main__': stormarn(googlesheets())
