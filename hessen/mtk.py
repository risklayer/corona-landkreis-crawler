#!/usr/bin/python3
from botbase import *

_mtk_a = re.compile(r"Aktuelle Infizierte:\s+([0-9.]+)\s+[+-]?\s+([0-9.]+)")
_mtk_d = re.compile(r"Todesfälle nach RKI:\s+([0-9.]+)\s+[+-]?\s+([0-9.]+)")
_mtk_g = re.compile(r"Genesene:1?\s+([0-9.]+)\s+[+-]?\s+([0-9.]+)")
_mtk_c = re.compile(r"Infektionen nach RKI:\s+([0-9.]+)\s+[+-]?\s+([0-9.]+)")

def mtk(sheets):
    from pdfminer.layout import LAParams
    url = "https://www.mtk.org/statics/ds_doc/downloads/"+today().strftime("%y_%m%d")+"Coronazahlen.pdf"
    content = get_pdf_text(url, laparams=LAParams(boxes_flow=.8, char_margin=100))
    #print(content)
    a, aa = map(force_int, _mtk_a.search(content).groups())
    d, dd = map(force_int, _mtk_d.search(content).groups())
    g, gg = map(force_int, _mtk_g.search(content).groups())
    c, cc = map(force_int, _mtk_c.search(content).groups())
    c = max(c, a + d + g)
    cc = (aa + dd + gg) if c == (a+d+g) else None
    update(sheets, 6436, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, sig=str(a), comment="Bot ohne SI A"+str(a))
    return True

schedule.append(Task(14, 5, 15, 57, 600, mtk, 6436))
if __name__ == '__main__': mtk(googlesheets())
