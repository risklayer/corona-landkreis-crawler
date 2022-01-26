#!/usr/bin/python3
## Tommy

from botbase import *

def giessen(sheets):

    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://corona.lkgi.de/aktuelles/fallzahlen-im-landkreis/")
    date_text = soup.find("div", {"class":"fusion-text fusion-text-1"}).get_text().strip()
    if not today().strftime("%e. %B %Y") in date_text: raise NotYetAvailableException("Giessen noch alt:" + date_text)

    data_items = soup.find_all("div", {"class": "title-heading-center title-heading-tag fusion-responsive-typography-calculated"})
    data = {}
    for item in data_items:
        data[item.findNext("p").get_text()] = item.get_text()

    cc = force_int(data["Neuinfektionen seit gestern"])
    c = force_int(data["Coronafälle insgesamt"])
    d = force_int(data["Verstorbene"])
    g = force_int(data["Genesene"])
    s = force_int(data.get("Stationär Behandelte in Kliniken im Landkreis Gießen", None)) or None

    update(sheets, 6531, c=c, cc=cc, d=d, g=g, s=s, sig="Bot")
    return True

schedule.append(Task(17, 5, 18, 35, 360, giessen, 6531))
if __name__ == '__main__': giessen(googlesheets())
