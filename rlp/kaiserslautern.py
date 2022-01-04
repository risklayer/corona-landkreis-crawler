#!/usr/bin/python3
from botbase import *

_kl_cc = re.compile(r"Neufälle \(([0-9.]+) x? *Stadt(?: KL)? *[,;] ([0-9.]+) x? *(?:LK KL|Landkreis)(?:.? *([0-9.]+) x? *Streitkräfte)?\)")
_kl_gg = re.compile(r"\(([0-9.]+) x? *Stadt(?: KL)?[,;] ([0-9.]+) x? *(?:LK KL|Landkreis)(?:[, ;] *([0-9.]+) x? *Streitkräfte)?\)? *konnten die Quarantäne verlassen")
#_kl_gg = re.compile(r"\(([0-9.]+) x? *Stadt KL, ([0-9.]+) x? *LK KL?\) konnten die Quarantäne verlassen")
_kl_stadt = re.compile(r"Stadt KL: ([0-9.]+) *Indexfälle, ([0-9.]+) Genesene, (\d+) Todesfälle")
_kl_lk = re.compile(r"LK KL: ([0-9.]+) Indexfälle, ([0-9.]+) Genesene, (\d+) Todesfälle")
_kl_sk = re.compile(r"Streitkräfte \(on base\): ([0-9.]+) Indexfälle, ([0-9.]+) *Genesene(?:, (\d+) Todesfälle)?")

def kaiserslautern(sheets):
    soup = get_soup("https://www.kaiserslautern-kreis.de/aktuelles/corona-virus.html")
    content = soup.find(id="col3_content")
    p = content.findAll("p")[1].get_text(" ")
    #print(p)
    if not today().strftime("- %d.%m. :") in p: raise NotYetAvailableException("Kaiserslautern noch alt:" + p[:50])
    cc1, cc2, cc3 = map(lambda x:force_int(x, 0), _kl_cc.search(p).groups())
    #gg1, gg2, gg3 = map(lambda x:force_int(x, 0), _kl_gg.search(p).groups())
    c1, g1, d1 = map(lambda x:force_int(x, 0), _kl_stadt.search(p).groups())
    c2, g2, d2 = map(lambda x:force_int(x, 0), _kl_lk.search(p).groups())
    c3, g3, d3 = map(lambda x:force_int(x, 0), _kl_sk.search(p).groups())
    update(sheets, 7312, c=c1, cc=cc1, d=d1, g=g1, sig="Bot", ignore_delta=True)
    update(sheets, 7335, c=c2+c3, cc=cc2+cc3, d=d2+d3, g=g2+g3, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(18, 2, 21, 35, 600, kaiserslautern, 7335))
if __name__ == '__main__': kaiserslautern(googlesheets())
