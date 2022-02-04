#!/usr/bin/python3
from botbase import *

_mtk_a = re.compile(r"Aktuelle Infizierte:\s+([0-9.]+)\s+[+-]?\s+([0-9.]+)")
_mtk_d = re.compile(r"Todesfälle nach RKI:\s+([0-9.]+)\s+[+-]?\s+([0-9.]+)")
_mtk_g = re.compile(r"Genesene:1?\s+([0-9.]+)\s+[+-]?\s+([0-9.]+)")

def mtk(sheets):
    from pdfminer.layout import LAParams
    url = "https://www.mtk.org/statics/ds_doc/downloads/"+today().strftime("%y_%m%d")+"Coronazahlen.pdf"
    content = get_pdf_text(url, laparams=LAParams(boxes_flow=.8, char_margin=100))
    #print(content)
    a = force_int(_mtk_a.search(content).group(1))
    d = force_int(_mtk_d.search(content).group(1))
    g = force_int(_mtk_g.search(content).group(1))
    c = a + d + g
    update(sheets, 6436, c=c, d=d, g=g, comment="Bot ohne SI")
    return True

schedule.append(Task(14, 5, 15, 57, 600, mtk, 6436))
if __name__ == '__main__': mtk(googlesheets())
