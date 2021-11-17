#!/usr/bin/python3
from botbase import *

# Beware: this site uses plenty of non-breaking spaces
_neunkirchen_cc = re.compile(r"gibt\ses\s+([0-9.]+|\w+)\s+weitere", re.U)
_neunkirchen_c = re.compile(r"insgesamt\salso\s(?:weiter\s)?\s*([0-9.]+)\s+positive", re.U)
_neunkirchen_d = re.compile(r"\s+([0-9.]+)\s+Covid-19-Todesfälle", re.U)
_neunkirchen_g = re.compile(r"können\s+([0-9.]+)\s*Personen\s[^\s]*\s*als\sgeheilt", re.U)
_neunkirchen_gg = re.compile(r"können\s+[0-9.]+\s*Personen\s+\(([+-]*[0-9]+)\)\s+als\sgeheilt", re.U)
_neunkirchen_a = re.compile(r"Stand\sheute\ssind\s+([0-9.]+)\s+Personen\s+im\s+Landkreis\sNeunkirchen\smit\sdem\sCoronavirus\sinfiziert")

def neunkirchen(sheets):
    soup = get_soup("https://www.landkreis-neunkirchen.de/index.php?id=3554")
    ps, todaystr = None, today().strftime("%d.%m.%Y")
    for i, b in enumerate(soup.find(id="ContentText").find(id="c18160").findAll(class_="csc-default")[:20]):
        #print("#",i,"\n", b.get("id"), "\n-------------------")
        #ps = ["".join([x for x in p.findAll(text=True)]).strip() for p in b.findAll("p")]
        #ps = [p for p in ps if p != ""]
        ps = b.get_text(" ").strip()
        if todaystr in ps: break
        ps = None
    if ps is None: raise NotYetAvailableException("Neunkirchen noch alt.")
    text = ps #"\n".join(ps)
    #print(text)
    c = force_int(_neunkirchen_c.search(text).group(1))
    cc = force_int(_neunkirchen_cc.search(text).group(1))
    d = force_int(_neunkirchen_d.search(text).group(1))
    g = force_int(_neunkirchen_g.search(text).group(1))
    gg = force_int(_neunkirchen_gg.search(text).group(1))
    a = force_int(_neunkirchen_a.search(text).group(1))
    d = c - g - a # alternative Berechnung D
    update(sheets, 10043, c=c, cc=cc, d=d, g=g, gg=gg, sig="Bot", ignore_delta=False)
    return True

schedule.append(Task(16, 30, 23, 55, 900, neunkirchen, 10043))
if __name__ == '__main__': neunkirchen(googlesheets())
