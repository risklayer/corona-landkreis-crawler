#!/usr/bin/python3
from botbase import *
import re, time
_rlpat = re.compile(r"lua.rlp.de|speyer.de|rhein-pfalz-kreis.de").search

def rlp(sheets):
    blacklist=[7317,7340,7320,7333] # Pirmasens, Südwestpfalz, Zweibrücken, Donnersbergkreis
    soup = get_soup("https://lua.rlp.de/de/presse/detail/news/News/detail/coronavirus-sars-cov-2-aktuelle-fallzahlen-fuer-rheinland-pfalz/")
    stand = soup.find(id="content").find("h5").text
    if not today().strftime("%d.%m.%Y") in stand: raise NotYetAvailableException("RLP noch alt? " + stand)
    batch = []
    for row in soup.find(id="content").findAll("tr")[3:-1]:
        row = [x.text.strip() for x in row.findAll("td")]
        #print(row)
        ags = ags_from_name(row[0])
        if ags in blacklist: continue
        if not ags:
            print("Name not mapped:", row[0])
            continue
        c, d, g = int(row[1]), int(row[4]), int(row[5])
        cc = int(row[2])
        update(sheets, ags, c=c, cc=cc, g=g, d=d, sig="Land", comment="Bot", check=_rlpat, batch=batch)
        time.sleep(1) # avoid rate limit problems
    do_batch(sheets, batch)
    return True

schedule.append(Task(14, 00, 15, 00, 120, rlp, 7134))
if __name__ == '__main__': rlp(googlesheets())
