#!/usr/bin/python3
from botbase import *
import re, time
_lglpat = re.compile(r"lgl.bayern.de").search

def lgl(sheets):
    soup = get_soup("https://www.lgl.bayern.de/gesundheit/infektionsschutz/infektionskrankheiten_a_z/coronavirus/karte_coronavirus/index.htm")
    table = soup.find(id="tableLandkreise")
    if not table: raise Exception("LGL HTML Tabelle tableLandkreise nicht gefunden.")
    if not todaystr in table.find("caption").text: raise Exception("LGL noch alt? " +table.find("caption").text)
    for row in table.findAll("tr")[1:-1]:
        row = [x.text.strip() for x in row.findAll("td")]
        ags = ags_from_name(row[0])
        if not ags:
            print("Name not mapped:", row[0])
            continue
        c, d = force_int(row[1]), force_int(row[6])
        cc, dd = force_int(row[2]), force_int(row[7])
        update(sheets, ags, c=c, cc=cc, d=d, dd=dd, sig="Land", comment="Bot", check=_lglpat)
        time.sleep(50) # to avoid rate limit problems
    return True

schedule.append(Task(14, 00, 15, 00, 120, lgl, 9774))
if __name__ == '__main__': lgl(googlesheets())
