#!/usr/bin/python3
## Tommy

from botbase import *

def alzeyworms(sheets):

    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    domain = "https://www.kreis-alzey-worms.eu/"
    soup = get_soup("https://www.kreis-alzey-worms.eu/verwaltung/aktuelles/")

    for item in soup.find_all("div", {"class":"listEntryInner"}):
        if "Corona:" in item.text:
            date_text = item.find("span", {"class":"listEntryDate"}).text
            check_date(date_text, "Alzey-Worms")
            link = item.find("a")["href"]
            break

    argsl, argss = dict(), dict()

    rows = get_soup(domain + link).find_all("table")[0].findAll("tr")
    headers = [x.text.strip() for x in rows[0].findAll("th")]
    rows = [[x.text.strip() for x in row.findAll("td")] for row in rows[1:]]

    assert headers[1] == "Fallzahl"
    argsl["c"] = force_int(rows[0][1])
    assert headers[2] == "Neue Fälle"
    argsl["cc"] = force_int(rows[0][2])
    assert headers[3] == "Weitere Todesfälle"
    argsl["dd"] = force_int(rows[0][3])
    assert headers[4] == "Todesfälle insgesamt"
    argsl["d"] = force_int(rows[0][4])
    assert headers[5] == "Im Krankenhaus"
    argsl["s"] = force_int(rows[0][5])

    argss["c"] = force_int(rows[1][1])
    argss["cc"] = force_int(rows[1][2])
    argss["dd"] = force_int(rows[1][3])
    argss["d"] = force_int(rows[1][4])
    argss["s"] = force_int(rows[1][5])

    rows_2 = get_soup(domain + link).find_all("table")[3].findAll("tr")
    headers_2 = [x.text.strip() for x in rows_2[0].findAll("th")]
    rows_2 = [[x.text.strip() for x in row.findAll("td")] for row in rows_2[1:]]

    assert headers_2[2] == "Genesene"
    argsl["g"] = force_int(rows_2[1][2])
    argss["g"] = force_int(rows_2[2][2])

    update(sheets, 7331, **argsl, sig="Bot", ignore_delta=True)
    update(sheets, 7319, **argss, sig="Bot", ignore_delta=True)

    return True

schedule.append(Task(15, 33, 17, 33, 360, alzeyworms, 7331))
if __name__ == '__main__': alzeyworms(googlesheets())
