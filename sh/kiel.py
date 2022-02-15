#!/usr/bin/python3
## Tommy
from botbase import *

_kiel_c = re.compile(r"Gesamtzahl\s+aller\s+Fälle:\s*([0-9.]+[0-9])")
_kiel_cc = re.compile(r"([0-9.]+) (?:neue Positivfälle|Neuinfektionen)", re.I)
_kiel_d = re.compile(r"Verstorben sind ([0-9.]+)")

def kiel(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.kiel.de/de/gesundheit_soziales/gesundheit_vorsorgen_heilen/infektionsschutz/coronavirus.php")

    date_text = soup.find(id="inhaltbereich").find("h6", class_="Base-categoryHeadline", text=re.compile(r"Stand"))
    if not (today() - datetime.timedelta(1)).strftime("%e. %B") in date_text.text: raise NotYetAvailableException("Kiel noch alt:" + date_text.text)
    teaser = date_text.findNext("p").text
    print(teaser)

    c = force_int(_kiel_c.search(teaser).group(1))
    cc = force_int(_kiel_cc.search(teaser).group(1))
    d = force_int(_kiel_d.search(teaser).group(1))
    update(sheets, 1002, c=c, cc=cc, d=d, sig="", comment="Später Land. LKBot", ignore_delta=True, date=today()-datetime.timedelta(1))
    return True

schedule.append(Task(15, 00, 17, 00, 360, kiel, 1002))
if __name__ == '__main__': kiel(googlesheets())



