#!/usr/bin/python3
## Tommy

from botbase import *

_lichtenfels_date = re.compile(r"Aktuell \(Stand: (\d\d?\.\d\d?\.20\d\d)")

def lichtenfels(sheets):

    soup = get_soup("https://www.lkr-lif.de/landratsamt/gesundheit-und-verbraucherschutz/gesundheitswesen/informationen-fuer-die-buerger/coronavirus/7419.Aktuelle-Zahlen-zu-den-COVID-19-Infizierten-und-Impfungen-im-Landkreis-Lichtenfels.html#COVID-19-Zahlen")
    date_text = next(x for x in soup.find_all("p") if "Aktuell (Stand:" in x.get_text()).get_text()
    date = _lichtenfels_date.search(date_text).group(1)
    check_date(date, "Lichtenfels")
    tables = soup.find_all("table")

    assert "Neuinfizierte" in tables[0].get_text()
    cc = force_int(tables[0].find_all("td")[1].get_text())

    rows = [[x.text.strip() for x in row.findAll(["td"])] for row in tables[1].findAll("tr")]
    assert "Genesen" in rows[2][0]
    assert "Fälle gesamt" in rows[3][0]
    c = force_int(rows[3][1])
    g = force_int(rows[2][1])

    update(sheets, 9478, c=c, cc=cc, g=g, sig="Bot")
    return True

schedule.append(Task(17, 10, 18, 40, 360, lichtenfels, 9478))
if __name__ == '__main__': lichtenfels(googlesheets())
