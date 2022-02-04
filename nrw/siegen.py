#!/usr/bin/python3
from botbase import *

_siegen_c = re.compile(r"insgesamt ([0-9.]+) Personen aus Siegen-Wittgenstein mit dem Coronavirus")
_siegen_cc = re.compile(r"([0-9.]+|\w+) neue Coronafälle")
_siegen_d = re.compile(r", ([0-9.]+)\*? verstorben\.")
_siegen_g = re.compile(r"([0-9.]+) sind wieder genesen")
_siegen_gg = re.compile(r"([0-9.]+|\w+) als genesen aus der")
_siegen_si = re.compile(r"([0-9.]+|\w+) Personen aus Siegen-Wittgenstein (?:in einem Krankenhaus|stationär) behandelt werden, (?:[^.]* )?([0-9.]+|\w+) (?:davon )?intensiv")
_siegen_si2 = re.compile(r"kommen ([0-9.]+|\w+) P\w+ von außerhalb des Kreisgebiets, die (?:stationär|auf Normalstation) behandelt werden(?: müssen, ([0-9.]+|\w+) davon intensiv)?")
_siegen_q = re.compile(r"([0-9.]+) Personen (?:in |unter )?häuslicher? Quarantäne")

def siegen(sheets):
    soup = get_soup("https://www.siegen-wittgenstein.de/Kreisverwaltung/Aktuelles/Pressemeldungen/")
    articles = soup.find("main").find("ol").findAll("li")
    article = next(a for a in articles if "Neuinfektionen" in a.get_text())
    #print(article.get_text())
    date = article.find("small").get_text() if article else None
    date = check_date(date.split(":")[-1], "Siegen")
    url = urljoin("https://www.siegen-wittgenstein.de/", article.find("a")["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    text = soup.find("main").find("article").get_text()
    #print(text)
    c = force_int(_siegen_c.search(text).group(1))
    cc = force_int(_siegen_cc.search(text).group(1))
    d = force_int(_siegen_d.search(text).group(1))
    g = force_int(_siegen_g.search(text).group(1))
    gg = force_int(_siegen_gg.search(text).group(1))
    s, i, q = None, None, None
    m = _siegen_q.search(text)
    if m: q = force_int(m.group(1))
    m = _siegen_si.search(text)
    if m: s, i = force_int(m.group(1)), force_int(m.group(2), 0)
    m2 = _siegen_si2.search(text)
    #print(m, m2)
    if m and m2: s, i = s + force_int(m2.group(1)), i + force_int(m2.group(2), 0)
    if not m2 and "von außerhalb" in text: s, i = None, None
    comment = "Bot, check SI" if s is not None and s > 0 else "Bot ohne SI"
    update(sheets, 5970, c=c, cc=cc, d=d, g=g, gg=gg, q=q, s=s, i=i, sig="Bot", comment=comment, ignore_delta="mon")
    return True

schedule.append(Task(9, 1, 14, 35, 360, siegen, 5970))
if __name__ == '__main__': siegen(googlesheets())
