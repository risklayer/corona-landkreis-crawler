#!/usr/bin/python3
from botbase import *
import re, time
_lglpat = re.compile(r"lgl.bayern.de").search

def lgl(sheets):
    soup = get_soup("https://www.lgl.bayern.de/gesundheit/infektionsschutz/infektionskrankheiten_a_z/coronavirus/karte_coronavirus/index.htm")
    table = soup.find(id="tableLandkreise")
    if not table: raise Exception("LGL HTML Tabelle tableLandkreise nicht gefunden.")
    if not today().strftime("%d.%m.%Y") in table.find("caption").text: raise NotYetAvailableException("LGL noch alt? " +table.find("caption").text)
    todo=[]
    for row in table.findAll("tr")[1:-1]:
        row = [x.text.strip() for x in row.findAll("td")]
        ags = ags_from_name(row[0])
        if not ags:
            print("Name not mapped:", row[0])
            continue
        c, d = force_int(row[1]), force_int(row[6])
        cc, dd = force_int(row[2]), force_int(row[7])
        if ags == 9564: d += 5 # Nürnberg
        if ags == 9275: d += 17 # LK Passau
        if ags == 9662: d += 3 # Schweinfurt
        todo.append( (ags,c,cc,d,dd) )
    rows = fetch_rows(sheets, [x[0] for x in todo])
    batch=[]
    for i,x in enumerate(todo):
        ags,c,cc,d,dd = x
        update(sheets, ags, c=c, cc=cc, d=d, dd=dd, sig="Land", comment="Land", check=_lglpat, batch=batch, row=rows[i])
        #time.sleep(5) # to reduce rate limit problems
    do_batch(sheets, batch)
    return True

schedule.append(Task(14, 00, 15, 00, 120, lgl, 9774))
if __name__ == '__main__': lgl(googlesheets())
