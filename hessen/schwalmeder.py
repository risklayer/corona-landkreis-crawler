#!/usr/bin/python3
from botbase import *

_stand = re.compile(r"Stand:\s*\w+,\s+(\d{1,2}\.\s+\w+\s+20\d\d)", re.U)
_match_two = re.compile(r"([0-9.]+)\s*\(([+-]?[0-9.]+)\)")

def schwalmeder(sheets):
    import dateparser
    soup = get_soup("https://www.schwalm-eder-kreis.de/Aktuelles/Aktuelle-Informationen-zum-neuartigen-Coronavirus-Covid-19/Aktuelle-Zahlen-Schwalm-Eder.htm")
    main = soup.find(id="content_frame")
    date = main.find("h4").get_text()
    #print(date, _stand.search(date))
    date = dateparser.parse(_stand.search(date).group(1))
    date = check_date(date, "Schwalmeder")
    rows = [[x.get_text() for x in y.findAll(["td","th"])] for y in main.findAll("tr")]
    #print(*rows, sep="\n")
    assert "Fälle insgesamt" in rows[0][0]
    c, cc = map(force_int, _match_two.search(rows[1][0]).groups())
    assert "entlassen" in rows[0][1]
    g = force_int(rows[1][1])
    assert "verstorben" in rows[0][2]
    d, dd = map(force_int, _match_two.search(rows[1][2]).groups())
    update(sheets, 6634, c=c, cc=cc, d=d, dd=dd, g=g, sig="Bot")
    return True

schedule.append(Task(14, 10, 16, 35, 360, schwalmeder, 6634))
if __name__ == '__main__': schwalmeder(googlesheets())
