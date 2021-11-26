#!/usr/bin/python3
from botbase import *

_bamberg_st = re.compile(r"Stand: (\d\d?\. \w+ 20\d\d, \d\d?:\d\d) Uhr")
_space_re = re.compile(r"^\s*(.*?)\s*$")

def bamberg(sheets):
    soup = get_soup("https://www.landkreis-bamberg.de/Kurzmen%C3%BC/Startseite/index.php?&object=tx,2892.5.1&ModID=7&FID=2976.2576.1&kat=&kuo=2&k_sub=0&La=1")
    main = soup.find("article")
    table = next(x.find_next("table") for x in soup.find_all("h3") if "Fallzahlen" in x.text)
    #print(table)
    rows = [[_space_re.match(x.get_text()).group(1) for x in row.findAll(["td","th"])] for row in table.findAll("tr")]
    #print(*rows, sep="\n")
    date = _bamberg_st.search(main.get_text()).group(1)
    date = check_date(date, "Bamberg")
    assert "Veränderung" in rows[0][2]
    assert "Aktive Fälle" in rows[3][0]
    assert "Stadt Bamberg" in rows[4][0]
    a_s = force_int(rows[4][1])
    assert "Landkreis Bamberg" in rows[5][0]
    a_l = force_int(rows[5][1])
    assert "Gesamtzahl Infizierte" in rows[6][0]
    assert "Stadt Bamberg" in rows[7][0]
    c_s, cc_s = map(force_int, rows[7][1:])
    assert "Landkreis Bamberg" in rows[8][0]
    c_l, cc_l = map(force_int, rows[8][1:])
    update(sheets, 9461, c=c_s, cc=cc_s, date=date, sig=str(a_s), comment="Bot nur C A"+str(a_s), ignore_delta="mon") # SK
    update(sheets, 9471, c=c_l, cc=cc_l, date=date, sig=str(a_l), comment="Bot nur C A"+str(a_l), ignore_delta="mon") # LK
    return True

schedule.append(Task(14, 30, 16, 35, 360, bamberg, 9471))
if __name__ == '__main__': bamberg(googlesheets())
