#!/usr/bin/python3
## Tommy

from botbase import *

def emmendingen(sheets):

    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.landkreis-emmendingen.de/aktuelles/coronavirus/fallzahlen-inzidenz-impfzahlen-und-lageberichte")
    args = dict()

    content = soup.find(id="c4813")
    date_text = content.findNext("p").text
    if not today().strftime("%e. %B %Y") in date_text: raise NotYetAvailableException("Emmendingen noch alt:" + date_text)

    rows = content.find("table").findAll("tr")
    rows = [[x.text.strip() for x in row.findAll("td")] for row in rows]

    assert "Neue Fälle im Landkreis Emmendingen" in rows[2][0]
    args["cc"] = force_int(rows[2][1])
    assert "Fälle gesamt im Landkreis Emmendingen" in rows[3][0]
    args["c"] = force_int(rows[3][1])
    assert "Neue Todesfälle im Landkreis Emmendingen" in rows[5][0]
    args["dd"] = force_int(rows[5][1])
    assert "Todesfälle gesamt im Landkreis Emmendingen" in rows[6][0]
    args["d"] = force_int(rows[6][1])

    #print(args)
    update(sheets, 8316, **args, sig="Bot")
    return True

schedule.append(Task(15, 45, 17, 45, 360, emmendingen, 8316))
if __name__ == '__main__': emmendingen(googlesheets())



