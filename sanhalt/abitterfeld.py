#!/usr/bin/python3
from botbase import *

_abitterfeld_st = re.compile(r"stand:\s*(\d\d?\.\d\d?.20\d\d)", re.U)

def abitterfeld(sheets):
    soup = get_soup("https://www.anhalt-bitterfeld.de/de/covid19/informations-hotline-zu-covid-19.html")
    article = soup.find("main").find("article")
    date = _abitterfeld_st.search(article.get_text())
    date = check_date(date.group(1) if date is not None else article.get_text(), "Anhalt-Bitterfeld")
    rows = [[x.get_text() for x in row.findAll("td")] for row in article.find("table").findAll("tr")]
    #print(*rows, sep="\n")
    assert "bisher" in rows[0][0]
    assert "aktuell" in rows[0][1]
    c = force_int(rows[1][0])
    a = force_int(rows[1][1])
    update(sheets, 15082, c=c, sig=str(a), comment="Bot ohne IDG A"+str(a))
    return True

schedule.append(Task(15, 00, 18, 35, 600, abitterfeld, 15082))
if __name__ == '__main__': abitterfeld(googlesheets())
