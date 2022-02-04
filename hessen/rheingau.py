#!/usr/bin/python3
from botbase import *

_rheingau_re = re.compile(r"Rheingau-Taunus-Kreis\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", re.M)

def rheingau(sheets):
    from pdfminer.layout import LAParams
    url = "https://www.rheingau-taunus.de/fileadmin/forms/corona-virus/coronavirus_fallzahlen_"+(today()-datetime.timedelta(1)).strftime("%Y_%m_%d")+".pdf"
    content = get_pdf_text(url, laparams=LAParams(boxes_flow=None)).replace("\n\n","\n")
    #print(content)
    a, g, c, d = map(int, _rheingau_re.search(content).groups())
    c, d, g = c + 6, d + 2, g + 4 - d
    update(sheets, 6439, c=c, d=d, g=g)
    return True

schedule.append(Task(8, 5, 8, 37, 360, rheingau, 6439))
if __name__ == '__main__': rheingau(googlesheets())
