#!/usr/bin/python3
## Tommy
from botbase import *

def giessen(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://corona.lkgi.de/")
    main = next(x for x in soup.findAll(class_="fusion-fullwidth") if "Stand:" in x.get_text())
    #print(main.get_text())
    date_text = main.find("p", text=re.compile(r"Stand:")).get_text().strip()
    if not today().strftime("%e. %B %Y") in date_text: raise NotYetAvailableException("Giessen noch alt:" + date_text)

    data_items = main.find_all("div", {"class": "title-heading-center title-heading-tag fusion-responsive-typography-calculated"})
    data = {}
    for item in data_items:
        k = item.findNext("p").get_text()
        if "7 Tage" in k: continue
        k = k.split("\n")[0]
        data[k] = item.get_text()
    #print(*data.items(), sep="\n")

    cc = force_int(data["Neuinfektionen"])
    c = force_int(data["Coronafälle"])
    d = force_int(data["Verstorbene"])
    g = None #force_int(data["Genesene"])
    s = force_int(data.get("Stationär Behandelte", None)) or None

    update(sheets, 6531, c=c, cc=cc, d=d, g=g, s=s, sig="Bot")
    return True

schedule.append(Task(17, 5, 18, 35, 360, giessen, 6531))
if __name__ == '__main__': giessen(googlesheets())
