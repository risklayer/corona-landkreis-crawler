#!/usr/bin/python3
from botbase import *

_barnim = re.compile(r"(\d+\.\d\d\d) +(?:\(([+-] *[.0-9]+)\))? +(\d+\.\d\d\d) +(?:\(([+-] *[.0-9]+)\))? +(\d\d\d) +(?:\(([+-] *[0-9]+)\))? +([0-9]*)\s*Die *gemeldeten *Fallzahlen", re.M)

def barnim(sheets):
    from pdfminer.layout import LAParams
    url = "https://covid19.barnim.de/fileadmin/portal/corona/Lagebericht/2022/"+today().strftime("%y-%m_%d")+"_Lagebericht_Corona-Homepage.pdf"
    content = get_pdf_text(url, laparams=LAParams(boxes_flow=.9, char_margin=200))
    #print(content)
    c, cc, g, gg, d, dd, a = map(force_int, _barnim.search(content).groups())
    update(sheets, 12060, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg)
    return True

schedule.append(Task(13, 35, 15, 57, 600, barnim, 12060))
if __name__ == '__main__': barnim(googlesheets())
