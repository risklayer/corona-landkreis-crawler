#!/usr/bin/python3
from botbase import *

_koblenz = re.compile(r"^Koblenz\s([0-9.]+)\s+\+?/?(-?[0-9.]+)\s+([0-9.]+)\s+\+?/?(-?[0-9.]+)\s+([0-9.]+)\s+\+?/?(-?[0-9.]+)\s+([0-9.]+)\s+\+?/?(-?[0-9.]+)\s+([0-9.]+)\s+\+?/?(-?[0-9.]+)", re.M)
_mkoblenz = re.compile(r"^Mayen-Koblenz\s([0-9.]+)\s+\+?/?(-?[0-9.]+)\s+([0-9.]+)\s+\+?/?(-?[0-9.]+)\s+([0-9.]+)\s+\+?/?(-?[0-9.]+)\s+([0-9.]+)\s+\+?/?(-?[0-9.]+)\s+([0-9.]+)\s+\+?/?(-?[0-9.]+)", re.M)

def koblenz(sheets):
    from pdfminer.layout import LAParams
    import locale, urllib.parse
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    url = "https://www.kvmyk.de/kv_myk/Corona/Corona-Statistiken/"+urllib.parse.quote(today().strftime("%B %Y"))+"/Fallzahlen%20"+today().strftime("%d.%m.%Y")+".pdf"
    #print(url)
    content = get_pdf_text(url, laparams=LAParams(boxes_flow=.8, char_margin=100))
    if not "Koblenz" in content: content = get_pdf_text(url, laparams=LAParams(boxes_flow=.8, char_margin=100), rotation=90)
    #print(content)
    c, cc, g, gg, a, aa, d1, dd1, d2, dd2 = map(force_int, _koblenz.search(content).groups())
    d, dd = d1 + d2, dd1 + dd2
    update(sheets, 7111, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, ignore_delta="mon") # Koblenz
    c, cc, g, gg, a, aa, d1, dd1, d2, dd2 = map(force_int, _mkoblenz.search(content).groups())
    d, dd = d1 + d2, dd1 + dd2
    update(sheets, 7137, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, ignore_delta="mon") # Mayen-Koblenz
    return True

schedule.append(Task(15, 15, 17, 57, 600, koblenz, 7137))
if __name__ == '__main__': koblenz(googlesheets())
