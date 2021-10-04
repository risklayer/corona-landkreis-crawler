#!/usr/bin/python3
from botbase import *

_wesel_c = re.compile(r"([0-9.]+) bestätigte")
_wesel_cc = re.compile(r"um ([0-9.]+) gestiegen")
_wesel_d = re.compile(r"([0-9.]+) Personen im Zusammenhang mit einer Corona-Infektion verstorben")
_wesel_d2 = re.compile(r"Todesfälle steigt auf ([0-9.]+)")
_wesel_g = re.compile(r"([0-9.]+) Menschen gelten als genesen")
_wesel_si = re.compile(r"([0-9.]+) Patienten mit einer Corona-Infektion in stationärer Behandlung, ([0-9.]+) Person(?:en)? werden intensiv", re.U)
_wesel_q = re.compile(r"([0-9.]+) Kreisbewohner in Quarantäne")

def wesel(sheets):
    from urllib.parse import urljoin
    soup = get_soup("https://www.kreis-wesel.de/de/inhalt/aktuelles/")
    articles = soup.find("main").findAll("dt")
    article = next(a for a in articles if "Infektionsfälle" in a.get_text())
    date = article.find_next_sibling(class_="ym-aside").text.split(" ")[-1] if article else None
    date = check_date(date, "Wesel")
    url = urljoin("https://www.kreis-wesel.de/", article.find("a")["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    cont = soup.find("main").find(class_="ym-content")
    tables = cont.findAll("table")
    tab1 = [[x.get_text() for x in row.findAll(["th","td"])] for row in tables[0].findAll("tr")]
    tab2 = [[x.get_text() for x in row.findAll(["th","td"])] for row in tables[2].findAll("tr")]
    #print(*tab1, "", *tab2, sep="\n")
    assert "Gesamtanzahl" in tab1[0][1]
    assert "Zuwachs" in tab1[0][2]
    assert "Genesen" in tab1[0][3]
    assert "Verstorben" in tab1[0][4]
    assert "Gesamt" in tab1[14][0]
    c, cc, g, d = map(force_int, tab1[14][1:])
    assert "Patienten" in tab2[0][1]
    assert "Intensiv" in tab2[0][2]
    assert "Aktueller Stand" in tab2[2][0]
    s, i = map(force_int, tab2[2][1:3])
    update(sheets, 5170, c=c, cc=cc, d=d, g=g, s=s, i=i, sig="Bot", ignore_delta=today().weekday()==0) # delta montags
    return True

schedule.append(Task(12, 30, 14, 35, 360, wesel, 5170))
if __name__ == '__main__': wesel(googlesheets())
