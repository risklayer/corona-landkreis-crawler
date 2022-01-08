#!/usr/bin/python3
## Tommy
from botbase import *

_kassel_data = re.compile(r"([0-9.]+)\s\(\+?([0-9.]+)")

def kassel(sheets):

    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.kassel.de/aktuelles/aktuelle-meldungen/coronavirus.php")
    header = soup.find(id="uebersicht-der-bestaetigten-sars-cov-2-faelle-in-stadt-und-landkreis-kassel")
    date_text = header.findNext("p").get_text()
    if not today().strftime("%e. %B %Y") in date_text: raise NotYetAvailableException("Kassel noch alt: " + date_text)
    rows = [[x.text.strip() for x in row.findAll(["th", "td"])] for row in header.findNext("table").findAll("tr")]

    assert "Genesene" in rows[0][3]
    assert "Todesfälle" in rows[0][4]
    assert "Fälle insgesamt" in rows[0][5]

    assert "Stadt" in rows[1][0]
    gs = force_int(_kassel_data.search(rows[1][3]).group(1))
    ggs = force_int(_kassel_data.search(rows[1][3]).group(2))
    ds = force_int(_kassel_data.search(rows[1][4]).group(1))
    dds = force_int(_kassel_data.search(rows[1][4]).group(2))
    cs = force_int(_kassel_data.search(rows[1][5]).group(1))
    ccs = force_int(_kassel_data.search(rows[1][5]).group(2))

    assert "Landkreis" in rows[2][0]
    gk = force_int(_kassel_data.search(rows[2][3]).group(1))
    ggk = force_int(_kassel_data.search(rows[2][3]).group(2))
    dk = force_int(_kassel_data.search(rows[2][4]).group(1))
    ddk = force_int(_kassel_data.search(rows[2][4]).group(2))
    ck = force_int(_kassel_data.search(rows[2][5]).group(1))
    cck = force_int(_kassel_data.search(rows[2][5]).group(2))

    update(sheets, 6611, c=cs, cc=ccs, g=gs, gg=ggs, d=ds, dd=dds, sig="Bot", ignore_delta="mon")
    update(sheets, 6633, c=ck, cc=cck, g=gk, gg=ggk, d=dk, dd=ddk, sig="Bot", ignore_delta="mon")

    return True

schedule.append(Task(11, 26, 13, 26, 360, kassel, 6611))
if __name__ == '__main__': kassel(googlesheets())
