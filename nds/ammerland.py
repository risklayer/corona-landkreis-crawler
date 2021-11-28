#!/usr/bin/python3
## Tommy

from botbase import *

_ammerland_d = re.compile(r"([0-9.]+) Personen sind verstorben")

def ammerland(sheets):

    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.ammerland.de/Aktuelles/Topthemen/Corona-Testung-/Coronavirus-INFOPORTAL/")
    args = dict()
    ts = soup.find_all("table")

    infection_table = False
    quar_table = False

    for t in ts:
        if "Infizierte Personen nach Gemeinden" in t.text:
            infection_table = t
            h2 = infection_table.findPrevious("h2").text
            if not today().strftime("%e. %B %Y") in h2: raise NotYetAvailableException("Ammerland noch alt:" + h2)
            quar_table = infection_table.findNext("table")
            break

    assert infection_table, quar_table

    infection_data = infection_table.tbody.find_all("tr")[9]  # erste Tabelle
    quar_data = quar_table.tbody.find_all("tr")[3]  # zweite Tabelle

    args["g"] = force_int(infection_data.find_all("td")[1].text.strip())
    args["cc"] = force_int(infection_data.find_all("td")[3].text.strip())
    aktuell = force_int(infection_data.find_all("td")[4].text.strip())

    temp = quar_data.find_all("td")[-1]
    args["q"] = force_int(temp.text.strip()) + aktuell
    args["d"] = force_int(_ammerland_d.search(temp.findNext("p").findNext("p").text).group(1))

    args["c"] = aktuell + args["g"] + args["d"]

    #print(args)
    update(sheets, 3451, **args, sig="Bot")
    return True

schedule.append(Task(14, 30, 16, 30, 360, ammerland, 3451))
if __name__ == '__main__': ammerland(googlesheets())




