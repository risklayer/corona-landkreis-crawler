#!/usr/bin/python3
from botbase import *

_waldeck_c = re.compile(r"Infiziert \(summiert[^)]+\)\s+([0-9.]+)")
_waldeck_cc = re.compile(r"Neuinfektionen\s+([0-9.]+)")
_waldeck_d = re.compile(r"Todesfälle \(summiert\)\s+([0-9.]+)")
_waldeck_g = re.compile(r"Genesen \(aktuell\)\s+([0-9.]+)")
_waldeck_s = re.compile(r"stationärer Behandlung[^0-9\n]+\s+([0-9.]+)")
_waldeck_i = re.compile(r"Intensiv[^0-9\n]+\s+([0-9.]+)")

def waldeck(sheets):
    from pdfminer.layout import LAParams
    url = "https://www.landkreis-waldeck-frankenberg.de/leben-geniessen/wohlbefinden-bewahren/gesundheitsfoerderung/informationen-zum-coronavirus/"+today().strftime("%Y-%m-%d")+"-lagebild-fallzahlen-covid-19.pdf"
    content = get_pdf_text(url, laparams=LAParams(boxes_flow=.8, char_margin=100))
    # print(content)
    c = force_int(_waldeck_c.search(content).group(1))
    cc = force_int(_waldeck_cc.search(content).group(1))
    g = force_int(_waldeck_g.search(content).group(1))
    d = force_int(_waldeck_d.search(content).group(1))
    s = force_int(_waldeck_s.search(content).group(1))
    i = force_int(_waldeck_i.search(content).group(1))
    update(sheets, 6635, c=c, cc=cc, d=d, g=g, s=s, i=i, ignore_delta="mon")
    return True

schedule.append(Task(15, 5, 16, 57, 600, waldeck, 6635))
if __name__ == '__main__': waldeck(googlesheets())
