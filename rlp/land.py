#!/usr/bin/python3
from botbase import *
import re, time
_rlpat = re.compile(r"lua.rlp.de|speyer.de|rhein-pfalz-kreis.de|rhein-lahn-kreis|landkreis-kusel|badkreuznach|kreis-sim.de|bitburg-pruem|kaiserslautern").search
_rlpstand = re.compile(r"Datenstand: (\d\d?\.\d\d?.20\d\d(?:, \d\d?:\d\d)?)")

def rlp(sheets):
    blacklist=[7317,7340,7320,7141,7211,7235] # Pirmasens, Südwestpfalz, Zweibrücken, Rhein-Lahn,Trier,Trier-Saarburg
    soup = get_soup("https://lua.rlp.de/de/presse/detail/news/News/detail/coronavirus-sars-cov-2-aktuelle-fallzahlen-fuer-rheinland-pfalz/")
    cont = soup.find(id="content").find(text=re.compile(r"Laborbestätigt, seit Beginn der Pandemie")).find_parent("table")
    stand = soup.find(id="content").find(text=_rlpstand)
    #print(stand)
    date = check_date(_rlpstand.search(stand).group(1), "RLP")
    #if not today().strftime("%d.%m.%Y") in stand: raise NotYetAvailableException("RLP noch alt? " + stand)
    todo = []
    for row in cont.findAll("tr")[3:-1]:
        row = [x.text.strip() for x in row.findAll("td")]
        #print(row)
        ags = ags_from_name(row[0])
        if ags in blacklist: continue
        if not ags:
            print("Name not mapped:", row[0])
            continue
        c, d, g = int(row[1]), int(row[4]), int(row[5])
        cc = int(row[2])
        comment = "Land"
        if ags == 7312: c, comment = c - 10, "Land offset"
        if ags == 7335: c, comment = c + 471, "Land offset"
        todo.append([ags,c,cc,g,d,comment])
    rows = fetch_rows(sheets, [x[0] for x in todo])
    batch = []
    for i,x in enumerate(todo):
        ags,c,cc,g,d,comment = x
        if ags == 7133: g = None # Donnersberg divergiert stark derzeit
        #if ags == 7132: g = None # divergiert stark derzeit
        update(sheets, ags, c=c, cc=cc, g=g, d=d, sig="Land", comment=comment, check=_rlpat, batch=batch, row=rows[i], date=date)
    do_batch(sheets, batch)
    return True

schedule.append(Task(14, 00, 16, 00, 120, rlp, 7134))
if __name__ == '__main__': rlp(googlesheets())
