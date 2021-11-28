#!/usr/bin/python3
## Tommy

from botbase import *

_kiel_c = re.compile(r"Gesamtzahl aller Fälle: ([0-9.]+)")
_kiel_cc = re.compile(r"([0-9.]+) neue Positivfälle")
_kiel_d = re.compile(r"Verstorben sind ([0-9.]+)")


def kiel(sheets):

    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.kiel.de/de/gesundheit_soziales/gesundheit_vorsorgen_heilen/infektionsschutz/coronavirus.php")
    args = dict()

    date_text = soup.find(id="inhaltbereich").find("h6", {"class": "Base-categoryHeadline u-marginTop--1"})

    if not today().strftime("%e. %B") in date_text.text: raise NotYetAvailableException("Kiel noch alt:" + date_text.text)

    teaser = date_text.findNext("p").text

    c_groups = _kiel_c.search(teaser)
    if c_groups: args["c"] = force_int(c_groups.group(1))
    cc_groups = _kiel_cc.search(teaser)
    if cc_groups: args["cc"] = force_int(cc_groups.group(1))
    d_groups = _kiel_d.search(teaser)
    if d_groups: args["d"] = force_int(d_groups.group(1))
    #print(args)
    update(sheets, 1002, **args, sig="Bot")
    return True

schedule.append(Task(15, 00, 17, 00, 360, kiel, 1002))
if __name__ == '__main__': kiel(googlesheets())


