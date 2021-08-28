#!/usr/bin/python3
from botbase import *

def berlin(sheets):
    import re
    def _extract(text): return int(re.search(r"(-?[0-9 ]+)", text)[0].replace(" ",""))
    soup = get_soup("https://data.lageso.de/lageso/corona/corona.html")
    stand = soup.find(class_="toptitle").find("p").text
    if not todaystr in stand: raise Exception("Berlin noch alt? " + stand)
    ags = 11000
    c = _extract(soup.find(id="box-fallzahl").find(class_="inner").text)
    d = _extract(soup.find(id="box-todesfaelle").find(class_="inner").text)
    g = _extract(soup.find(id="box-genesene").find(class_="inner").text)
    cc = _extract(soup.find(id="box-fallzahl_diff").find(class_="inner").text)
    dd = _extract(soup.find(id="box-todesfaelle_diff").find(class_="inner").text)
    gg = _extract(soup.find(id="box-genesene_diff").find(class_="inner").text)
    s, i = None, None
    ivena = soup.find(id="selbstauskunft-der-krankenhäuser-in-ivena")
    if ivena:
        for row in ivena.findAll("tr"):
            row = [x.text for x in row.findAll("td")]
            if "stationärer Behandlung" in row[0]: s = int(row[1])
            if "ITS" in row[0]: i = int(row[1])
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, s=s, i=i, d=d, dd=dd, sig="Bot")
    return True

schedule.append(Task(9, 0, 11, 0, 300, berlin, 11000))
if __name__ == '__main__': berlin(googlesheets())
