#!/usr/bin/python3
from botbase import *

_twovals = re.compile(r"\s*([0-9.]+)\s*\(\+?\/?(-?[0-9.]+)\)", re.U)

def halle(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.halle.de/de/Verwaltung/Presseportal/Nachrichten/index.aspx?NewsId=45334")
    article = soup.find(id="content-inner")
    if not today().strftime("%d. %B %Y") in article.find("strong").get_text():
        raise NotYetAvailableException("Halle (Saale) noch alt: "+article.find("strong").get_text());
    tables = article.findAll("table")
    args = dict()
    for table in tables[:4]:
        tab = [[x.get_text() for x in row.findAll(["td","th"])] for row in table.findAll("tr")]
        if len(tab)<2: continue
        #print(*tab, sep="\n")
        #print()
        if not "s" in args and len(tab[0]) > 2 and "Krankenhaus" in tab[0][2]:
            args["s"] = force_int(_twovals.search(tab[1][2]).group(1))
            assert "Intensiv" in tab[0][3]
            args["i"] = force_int(_twovals.search(tab[1][3]).group(1))
        if not "c" in args and len(tab[0]) > 2 and "Infizierte gesamt" in tab[0][0]:
            args["c"], args["cc"] = map(force_int, _twovals.search(tab[1][0]).groups())
            assert "Genesene" in tab[0][1]
            args["g"], args["gg"] = map(force_int, _twovals.search(tab[1][1]).groups())
            assert "Todesfälle" in tab[0][2]
            args["d"], args["dd"] = map(force_int, _twovals.search(tab[1][2]).groups())
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 15002, **args, sig="Bot")
    return True

schedule.append(Task(10, 00, 11, 35, 360, halle, 15002))
if __name__ == '__main__': halle(googlesheets())
