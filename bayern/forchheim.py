#!/usr/bin/python3
from botbase import *

_forchheim_st = re.compile(r"Stand: (\d\d\.\d\d\.20\d\d); (\d\d:\d\d) Uhr")
_forchheim_split = re.compile(r"^\n*\+?\s*(-?[0-9]+)? *\n\n\+?\s*(-?[0-9]+) *\n\n\+?\s*(?:(-?[0-9]+))?\n_+\n\+?\s*(-?[0-9]+)[\n\s]*$")

def forchheim(sheets):
    return True # derzeit nicht mehr
    def _fo_clean(x):
        for br in x.findAll("br"): br.replace_with("\n" + br.text)
        return x.get_text()
    soup = get_soup("https://lra-fo.de/site/1_1corona/informationen.php")
    table = soup.find(id="middle").find("table")
    rows = [[_fo_clean(x) for x in row.findAll(["td","th"])] for row in table.findAll("tr")]
    #print(*rows, sep="\n")
    date = " ".join(_forchheim_st.search(rows[-1][0]).groups())
    date = check_date(date, "Forchheim")
    assert "Veränderung" in rows[0][2]
    assert "insgesamt" in rows[1][0]
    #print(*rows[1][1:], sep="\n---\n")
    a, g, d, c = map(force_int, _forchheim_split.match(rows[1][1]).groups())
    aa, gg, dd, cc = map(force_int, _forchheim_split.match(rows[1][2]).groups())
    update(sheets, 9474, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(14, 0, 18, 35, 360, forchheim, 9474))
if __name__ == '__main__': forchheim(googlesheets())
