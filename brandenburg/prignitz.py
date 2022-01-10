#!/usr/bin/python3
from botbase import *

_prignitz_date = re.compile(r"Stand:\s(\d\d?\.\d\d?\.20\d\d)")

def prignitz(sheets):
    soup = get_soup("https://www.landkreis-prignitz.de/de/aktuelles/corona.php")
    header = next(x for x in soup.find_all("h2") if "Gesamtinfektionen nach Gemeinden (Stand:" in x.get_text())
    date_text = _prignitz_date.search(header.get_text()).group(1)
    check_date(date_text, "Prignitz")
    rows = [[x.text.strip() for x in row.findAll(["td","th"])] for row in header.findNext("table").findAll("tr")]
    assert "Anzahl der infizierten Personen seit Pandemiebeginn" in rows[0][1]
    assert "Neue Fälle" in rows[0][2]
    assert "Verstorben" in rows[0][3]
    assert "Kumulativ" in rows[-1][0]
    c = force_int(rows[-1][1])
    cc = force_int(rows[-1][2])
    d = force_int(rows[-1][3])
    update(sheets, 12070, c=c, cc=cc, d=d, ignore_delta="mon")
    return True

schedule.append(Task(14, 5, 16, 5, 360, prignitz, 12070))
if __name__ == '__main__': prignitz(googlesheets())
