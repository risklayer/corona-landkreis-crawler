#!/usr/bin/python3
from botbase import *

_olpe_c = re.compile(r"insgesamt seit Beginn der Pandemie \(03/2020\)\s+([0-9.]+)")
_olpe_cc = re.compile(r"Veränderung zu\w* \w*tag:?\s+([0-9.]+)")
_olpe_d = re.compile(r"Verstorben\s+([0-9.]+)")
_olpe_g = re.compile(r"Genesene Personen\s+([0-9.]+)")
_olpe_s = re.compile(r"Stationäre Behandlung\s+([0-9.]+)")
_olpe_i = re.compile(r"Intensivstation (?:min|ohne) Beatmung\s+([0-9.]+)")
_olpe_st = re.compile(r"Stand: *(\d\d?\.\d\d?\.20\d\d)")

def olpe(sheets):
    soup = get_soup("https://www.kreis-olpe.de/Themen/Coronavirus/Corona-Virus-Alle-Infos-auf-einen-Blick/Corona-Virus-Alle-Infos-auf-einen-Blick.php?redir=1")
    soup = soup.find(id="readthis")
    li = next(x for x in soup.findAll("li") if not x.find("li") and "Stand:" in x.get_text())
    date = check_date(_olpe_st.search(li.get_text()).group(1), "Olpe")
    url = urljoin("https://www.kreis-olpe.de/Themen/Coronavirus/Corona-Virus-Alle-Infos-auf-einen-Blick/Corona-Virus-Alle-Infos-auf-einen-Blick.php?redir=1", li.find("a", href=True)["href"])
    print("Loading", url)
    from pdfminer.layout import LAParams
    content = get_pdf_text(url, laparams=LAParams(boxes_flow=.8, char_margin=100))
    #print(content)
    c = force_int(_olpe_c.search(content).group(1))
    cc = force_int(_olpe_cc.search(content).group(1))
    d = force_int(_olpe_d.search(content).group(1))
    g = force_int(_olpe_g.search(content).group(1))
    s = force_int(_olpe_s.search(content).group(1))
    i = sum(force_int(x) for x in _olpe_i.findall(content))
    update(sheets, 5966, c=c, cc=cc, d=d, g=g, s=s, i=i, ignore_delta="mon")
    return True

schedule.append(Task(15, 5, 19, 57, 600, olpe, 5966))
if __name__ == '__main__': olpe(googlesheets())
