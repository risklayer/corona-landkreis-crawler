#!/usr/bin/python3
from botbase import *

_unna_c = re.compile(r"Gesamtinfizierte +([0-9.]+)")
#_unna_a = re.compile(r"Aktive Fälle +([0-9.]+) +kumulativ")
_unna_g = re.compile(r"Genesene +([0-9.]+) +kumulativ")
_unna_d = re.compile(r"Verstorbene *([0-9.]+)")

def unna(sheets):
    soup = get_soup("https://www.kreis-unna.de/nachrichten/n/?tx_news_pi1%5Bnews%5D=14220&tx_news_pi1%5Bcontroller%5D=News&tx_news_pi1%5Baction%5D=detail&cHash=31b36b644c47f5bc4011e1a3e334e130")
    main = soup.find(itemtype="http://schema.org/Article")
    text = main.get_text(" ").strip()
    #print(text)
    if not today().strftime("Stand: %d.%m.%Y") in text: raise NotYetAvailableException("Unna noch alt:" + text[:50])
    zahlen = main.find(class_="zahlen").get_text(" ").strip()
    #print(zahlen)
    c = force_int(_unna_c.search(text).group(1))
    d = force_int(_unna_d.search(text).group(1))
    g = force_int(_unna_g.search(text).group(1))
    stat = [x.get_text() for x in main.find(class_="zahlen-stationaer").findAll("td")]
    #print(stat)
    assert "Kreisweit" in stat[0]
    s = force_int(stat[2])
    update(sheets, 5978, c=c, d=d, g=g, s=s, sig="Bot")
    return True

schedule.append(Task(14, 30, 17, 35, 600, unna, 5978))
if __name__ == '__main__': unna(googlesheets())
