#!/usr/bin/python3
from botbase import *

_osterz_st = re.compile(r"Stand (\d\d\.\d\d\.20\d\d, \d\d:\d\d) Uhr")
_osterz_c = re.compile(r"Seit 02.03.2020 positiv getestete Personen:\s*([0-9.]+)\s*\(\+?(-?\s*[0-9.]+)\)")
_osterz_d = re.compile(r"verstorbene Personen:\s*([0-9.]+)\s*\(\+?(-?\s*[0-9.]+)\)")
_osterz_g = re.compile(r"Quarantäne entlassene Personen:\s*([0-9.]+)\s*\(\+?(-?\s*[0-9.]+)\)")
_osterz_si = re.compile(r"befinden sich\s*([0-9.]+)\s*positiv auf SARS-CoV-2 getestete Personen im Landkreis in Krankenhäusern. Davon\s*([0-9.]+)\s*intensiv")

def osterz(sheets):
    from urllib.parse import urljoin
    soup = get_soup("https://www.landratsamt-pirna.de/aktuelles-presse.html")
    articles = soup.findAll(class_="xm_block")
    article = next(a for a in articles if "Corona-Virus: Aktuelle" in a.get_text())
    date = article.find(class_="xm_typo--sub-head").text if article else None
    date = check_date(date, "Sächs. Schweiz Osterzgebirge")
    url = urljoin("https://www.landratsamt-pirna.de/", article.find(href=True)["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    text = soup.find(class_="xm_main__content").get_text(" ").strip()
    text = re.sub(r"(?:\s*\n\s*)+", "\n", text)
    #print(text)
    date = check_date(_osterz_st.search(text).group(1), "Sächs. Schweiz Osterzgebirge")
    c, cc = map(force_int, _osterz_c.search(text).groups())
    d, dd = map(force_int, _osterz_d.search(text).groups())
    g, gg = map(force_int, _osterz_g.search(text).groups())
    s, i = map(force_int, _osterz_si.search(text).groups())
    update(sheets, 14628, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, s=s, i=i, date=date, sig="Bot")
    return True

schedule.append(Task(12, 30, 17, 35, 360, osterz, 14628))
if __name__ == '__main__': osterz(googlesheets())
