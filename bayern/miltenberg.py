#!/usr/bin/python3
from botbase import *

_miltenberg_c = re.compile(r"Coronavirus-Infektionen beläuft sich auf ([0-9.]+) Fälle")
_miltenberg_cc = re.compile(r"([0-9.]+) Neuinfektionen")
_miltenberg_d = re.compile(r"gab (?:bisher )?([0-9.]+) Todesfälle")
_miltenberg_d2 = re.compile(r"Todesfälle (?:\w+ )+([0-9.]+)\.")
_miltenberg_a = re.compile(r"Aktuell befinden sich ([0-9.]+) mit SARS-CoV-2 infizierte")
_miltenberg_a2 = re.compile(r"aktuell mit SARS-CoV-2 infizierten Personen liegt bei ([0-9.]+)")
_miltenberg_q = re.compile(r"([0-9.]+) Menschen als Kontaktperson I in Quarantäne")
_miltenberg_si = re.compile(r"([0-9.]+|\w+) (?:Persone?n?|Mensche?n?) (?:wegen oder mit einer Covid-19-Infektion )?aus dem Landkreis (?:in )?stationäre?r? [bB]ehand\w+(?:, davon (?:sind )?([0-9.]+|\w+) (?:Persone?n?|Mensche?n?)?\s*intensiv)?", re.U)

def miltenberg(sheets):
    soup = get_soup("https://www.landkreis-miltenberg.de/Landkreis/Aktuell.aspx")
    articles = soup.find(id="aktuell").findAll("li")
    todaystr = today().strftime("%d.%m.%Y")
    article = [a for a in articles if todaystr in a.get_text() and "Fallzahlen im Landkreis" in a.get_text()]
    if not article:
        raise NotYetAvailableException(articles[0].get_text(" "))
    article = article[0]
    #date = check_date(todaystr, "Miltenberg")
    url = urljoin("https://www.landkreis-miltenberg.de/Landkreis/", article.find("a")["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    text = soup.find(id="news_beschreibung").get_text()
    #print(text)
    a = force_int((_miltenberg_a.search(text) or _miltenberg_a2.search(text)).group(1))
    c = force_int(_miltenberg_c.search(text).group(1))
    cc = force_int(_miltenberg_cc.search(text).group(1))
    d = force_int((_miltenberg_d.search(text) or _miltenberg_d2.search(text)).group(1))
    q = force_int(_miltenberg_q.search(text).group(1))
    g = c - d - a
    q = q + a
    s, i = map(force_int, _miltenberg_si.search(text).groups())
    comment = "Bot" if i is not None else "Bot ohne I"
    update(sheets, 9676, c=c, cc=cc, d=d, g=g, q=q, s=s, i=i, comment=comment, ignore_delta=True)
    return True

schedule.append(Task(9, 34, 15, 35, 600, miltenberg, 9676))
if __name__ == '__main__': miltenberg(googlesheets())
