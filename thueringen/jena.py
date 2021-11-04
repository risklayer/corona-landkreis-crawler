#!/usr/bin/python3
from botbase import *

_jena_st = re.compile(r"vom (\d\d\.\d\d.20\d\d)")
_jena_cc = re.compile(r"in den vergangenen 24 h:\s*([0-9.]+)")
_jena_c = re.compile(r"Infizierte insgesamt seit dem [0-9.]+:\s*([0-9.]+)")
_jena_d = re.compile(r"Verstorbene insgesamt:\s*([0-9.]+)")
_jena_g = re.compile(r"Genesene insgesamt:\s*([0-9.]+)")
_jena_s = re.compile(r"[Ss]tationäre Fälle:\s*([0-9.]+)")
_jena_i = re.compile(r"ITS:\s*([0-9.]+)")

def jena(sheets):
    soup = get_soup("https://gesundheit.jena.de/de/coronavirus")
    article = soup.find("main").find("article")
    par = next(p for p in article.find_all(class_="paragraph") if "Jenaer Statistik" in p.get_text())
    text = par.get_text(" ").strip()
    #print(text)
    date = check_date(_jena_st.search(text).group(1), "Jena", datetime.timedelta(1)) + datetime.timedelta(1)
    c = force_int(_jena_c.search(text).group(1))
    cc = force_int(_jena_cc.search(text).group(1))
    d = force_int(_jena_d.search(text).group(1))
    g = force_int(_jena_g.search(text).group(1))
    s, i = None, None
    try:
        s = force_int(_jena_s.search(text).group(1))
    except: pass
    try:
        i = force_int(_jena_i.search(text).group(1))
    except: pass
    update(sheets, 16053, c=c, cc=cc, d=d, g=g, s=s, i=i, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(10, 0, 15, 35, 360, jena, 16053))
if __name__ == '__main__': jena(googlesheets())
