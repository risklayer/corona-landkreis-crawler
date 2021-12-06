#!/usr/bin/python3
## Tommy

from botbase import *

def wunsiedel(sheets):

    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.landkreis-wunsiedel.de/buergerservice/aktuelle-informationen-zum-coronavirus-sars-cov-2#")

    date_text = soup.find(id="articleheadline5").text.strip()
    if not today().strftime("%d. %B %Y") in date_text: raise NotYetAvailableException("Wunsiedel noch alt:" + date_text)

    data_items = soup.find_all("div", {"data-mh": "CounterItem"})
    data = {}
    for item in data_items:
        data[item.find("h3").text.strip()] = item.find("div", {"class": "round-green"}).text.strip()
    cc = force_int(data["Neue Fälle"])
    c = force_int(data["Fälle gesamt"])
    d = force_int(data["Todesfälle"])
    g = force_int(data["Genesene"])
    i = force_int(data["belegte Covid19- Intensivbetten Klinikum"])

    update(sheets, 9479, c=c, cc=cc, d=d, g=g, i=i, sig="Bot")

    return True

schedule.append(Task(14, 40, 16, 40, 360, wunsiedel, 9479))
if __name__ == '__main__': wunsiedel(googlesheets())
