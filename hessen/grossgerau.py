#!/usr/bin/python3
from botbase import *

_gg_c = re.compile(r"Gesamtfallzahl\s+([0-9.]+)(?:,0)?\s+Differenz zur Vorwoche: \+?(-?[0-9.]+)", re.U)
_gg_g = re.compile(r"Genesene Fälle\s+([0-9.]+)\s+Differenz zur Vorwoche: \+?(-?[0-9.]+)", re.U)
_gg_d = re.compile(r"Todesfälle\s+([0-9.]+)\s+Differenz zur Vorwoche: \+?(-?[0-9.]+)", re.U)

def grossgerau(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://kreis-gross-gerau.wheregroup.com/cgi-bin/Gesundheit_und_Verbraucherschutz/GuV_COVID_19.xml?_signature=40%3A6NpgZbCRrh9vT12shzzTO_VyI7o&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&FORMAT=image%2Fpng&TRANSPARENT=true&QUERY_LAYERS=covid_19_aktuell_kreis&LAYERS=covid_19_aktuell_kreis&STYLES=&_OLSALT=0.7450999172969061&INFO_FORMAT=text%2Fhtml&EXCEPTIONS=XML&FEATURE_COUNT=100&I=50&J=50&CRS=EPSG%3A25832&WIDTH=101&HEIGHT=101&BBOX=453743.4039833457%2C5528144.243116475%2C461140.35306971474%2C5535541.192202843")
    content = soup.find("body")
    ps = [x.get_text() for x in content.findAll("div")]
    #for p in ps: print(p)
    date = ps[0].split("Aktualisierung")[1]
    date = check_date(date, "Gross-Gerau")
    c, cc = map(force_int, _gg_c.search(ps[2]).groups())
    g, gg = map(force_int, _gg_g.search(ps[4]).groups())
    d, dd = map(force_int, _gg_d.search(ps[5]).groups())
    assert c is not None
    update(sheets, 6433, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(11, 0, 14, 35, 360, grossgerau, 6433))
if __name__ == '__main__': grossgerau(googlesheets())
