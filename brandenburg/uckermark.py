#!/usr/bin/python3
from botbase import *

def uckermark(sheets):
    soup = get_soup("https://www.uckermark.de/index.phtml?La=1&sNavID=1897.1&mNavID=1897.1&object=tx,2203.741.1&kat=&kuo=2&sub=0")
    main = soup.find(class_="inhalt")
    tab = main.find(text=re.compile("positiv laborbestätigte COVID-19-Fälle")).find_parent("table")
    rows = [[x.get_text().strip() for x in row.findAll("td")] for row in tab.findAll("tr")]
    #print(*rows, sep="\n")
    date = tab.find_previous_sibling("p").get_text()
    #print(date, date.split(":",1)[-1])
    date = check_date(date.split(":",1)[-1], "Uckermark")
    row = rows[-3]
    assert "Summe Landkreis Uckermark" in row[0]
    assert "Vortag" in rows[1][0]
    assert "Gesamt" in rows[1][1]
    assert "verstorben" in rows[1][2]
    assert "Isolation" in rows[1][3]
    cc = force_int(row[1])
    c = force_int(row[2])
    d = force_int(row[3])
    a = force_int(row[4].split("(")[0])
    g = c - d - a
    update(sheets, 12073, c=c, cc=cc, d=d, g=g, ignore_delta="mon")
    return True

schedule.append(Task(10, 2, 12, 35, 600, uckermark, 12073))
if __name__ == '__main__': uckermark(googlesheets())
