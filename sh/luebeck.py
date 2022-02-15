#!/usr/bin/python3
from botbase import *

_luebeck = re.compile(r"insgesamt\s+([0-9.]+)\s*\(([+-]?[0-9.]*)\)\s+([0-9.]+)\s*\(([+-]?[0-9.]*)\)\s+([0-9.]+)\s*\(([+-]?[0-9.]*)\)\s+([0-9.]+)\s*\(([+-]?[0-9.]*)\)", re.U)
_luebeck_si = re.compile(r"Krankenhaus\s*(\d+)\s*\([+-]?\d*\) *davon auf der Intensivstation\s*(\d+)\s*\([+-]?\d*\)", re.U)

def luebeck(sheets):
    from pdfminer.layout import LAParams
    url = "https://www.luebeck.de/files/Corona/covid19-statistik/Lagebericht_COVID_19_Statistik_HL_Presse_"+today().strftime("%Y%m%d")+".pdf"
    content = get_pdf_text(url, laparams=LAParams(boxes_flow=.9, char_margin=200))
    #print(content)
    a, aa, g, gg, d, dd, c, cc = map(force_int, _luebeck.search(content).groups())
    s, i = map(force_int, _luebeck_si.search(content).groups())
    update(sheets, 1003, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, s=s, i=i, sig="", comment="Land später", ignore_delta=True)
    return True

schedule.append(Task(14, 35, 15, 57, 600, luebeck, 1003))
if __name__ == '__main__': luebeck(googlesheets())
