#!/usr/bin/python3
from botbase import *
import re
_shpat = re.compile(r"schleswig-holstein.de").search

def sh(sheets):
    soup = get_soup("https://www.schleswig-holstein.de/DE/Schwerpunkte/Coronavirus/Zahlen/zahlen_node.html")
    table = soup.find(id="cvd19_kreistabelle_kumulativ")
    if not table: raise Exception("SH HTML Tabelle cvd19_kreistabelle_kumulativ nicht gefunden.")
    stand = table.findNext("p").text
    if not today().strftime("%d.%m.%Y") in stand: raise NotYetAvailableException("Schleswig-Holstein noch alt? " + stand)
    todo = []
    for row in table.find("tbody").findAll("tr"):
        row = [x.text.strip() for x in row.findAll("td")]
        #print(row)
        ags = ags_from_name(row[0])
        if not ags:
            print("Name not mapped:", row[0])
            continue
        c, d = force_int(row[2]), force_int(row[6], 0)
        cc, dd = force_int(row[3]), force_int(row[7], 0)
        if ags == 1055: c = c - 1 # Ostholstein offset
        if ags == 1056: c = c + 17 # Pinneberg offset
        print("AGS", ags, c, cc, d, dd)
        todo.append( (ags,c,cc,d,dd) )
    rows = fetch_rows(sheets, [x[0] for x in todo])
    batch=[]
    for i,x in enumerate(todo):
        ags,c,cc,d,dd = x
        update(sheets, ags, c=c, cc=cc, d=d, dd=dd, sig="Land", comment="Land", check=_shpat, batch=batch, row=rows[i])
    do_batch(sheets, batch)
    return True

schedule.append(Task(18, 30, 22, 00, 180, sh, 1057))
if __name__ == '__main__': sh(googlesheets())
