#!/usr/bin/python3
from botbase import *

_vechta_c = re.compile(r"Landkreis Vechta *([0-9.]+) +([+-]?[0-9.]+)", re.U)
_vechta_d = re.compile(r"Todesfälle:\s*\n\s*([0-9.]+)", re.U)
_vechta_s = re.compile(r"im Krankenhaus: *([0-9.]+)", re.U)
_vechta_i = re.compile(r"([0-9.]+) Intensivpatienten", re.U)

def vechta(sheets):
    from pdfminer.layout import LAParams
    url = "https://www.landkreis-vechta.de/fileadmin/dokumente/pdf/aktuelles/veroeffentlichungen/Corona/Homepage/"+today().strftime("%d.%m.%Y")+".pdf"
    content = get_pdf_text(url, laparams=LAParams(boxes_flow=.9, char_margin=200))
    #print(content)
    c, cc = map(force_int, _vechta_c.search(content).groups())
    d = force_int(_vechta_d.search(content).group(1))
    s = force_int(_vechta_s.search(content).group(1))
    i = force_int(_vechta_i.search(content).group(1))
    update(sheets, 3460, c=c, cc=cc, d=d, s=s, i=i, ignore_delta=True)
    return True

schedule.append(Task(15, 15, 16, 57, 600, vechta, 3460))
if __name__ == '__main__': vechta(googlesheets())
