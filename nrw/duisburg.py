#!/usr/bin/python3
from botbase import *

_duispat = re.compile(r"Stand: *(\d\d?\.\d\d?\.20\d\d,? \d\d?:\d\d)")
_duisnum = re.compile(r"([0-9.]+)\s*\(\+?(-?[0-9]+)\)")

def duisburg(sheets):
    soup = get_soup("https://co-du.info/")
    main = soup.find(id="infektionsbox")
    h4 = main.find(text=_duispat)
    date = check_date(_duispat.search(h4).group(1) if h4 else main.find("h4").get_text(), "Duisburg", datetime.timedelta(hours=12))
    args,tmp=dict(), dict()
    assert "Bestätigt" in main.find(id="infektion11").get_text()
    assert "Verstorben" in main.find(id="infektion21").get_text()
    assert "Genesen" in main.find(id="infektion13").get_text()
    c, cc = map(force_int, _duisnum.search(main.find(id="infektion11").find("h3").get_text()).groups())
    d, dd = map(force_int, _duisnum.search(main.find(id="infektion21").find("h3").get_text()).groups())
    g, gg = map(force_int, _duisnum.search(main.find(id="infektion13").find("h3").get_text()).groups())
    assert "Kontakt" in main.find(id="infektion23").get_text()
    q = c - d - g + force_int(main.find(id="infektion23").find("h3").get_text())
    assert "station" in soup.find(id="station11").get_text()
    s = force_int(soup.find(id="station11").find("h3").get_text())
    assert "Intensiv" in soup.find(id="station21gr").get_text()
    i = force_int(soup.find(id="station21gr").find("h3").get_text())
    update(sheets, 5112, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, q=q, s=s, i=i, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(9, 2, 15, 35, 600, duisburg, 5112))
if __name__ == '__main__': duisburg(googlesheets())
