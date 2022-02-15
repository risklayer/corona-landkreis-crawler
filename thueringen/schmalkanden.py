#!/usr/bin/python3
from botbase import *

_schmalkanden_st = re.compile(r"(\d\d?\.\d\d\.?20\d\d)", re.U)
_schmalkanden_c = re.compile(r"Gesamtzahl[^0-9]*Laborbestätigung *([0-9.]+)", re.U)
_schmalkanden_cc = re.compile(r"Befundeingänge[^0-9]* +([0-9.]+)", re.U)
_schmalkanden_d = re.compile(r"Verstorbene[^0-9]*COVID.?19 +([0-9.]+)", re.U)
_schmalkanden_s1 = re.compile(r"stationär[^0-9]*an COVID.?19 +([0-9.]+)", re.U)
_schmalkanden_s2 = re.compile(r"stationär[^0-9]*mit COVID.?19 +([0-9.]+)", re.U)

def schmalkanden(sheets):
    from pdfminer.layout import LAParams
    url = "https://www.lra-sm.de/wp-content/uploads/"+today().strftime("%Y/%m")+"/PM-LRA_Bulletin-LK-SM_"+today().strftime("%d.%m.%Y")+".pdf"
    content = get_pdf_text(url, laparams=LAParams(boxes_flow=.9, char_margin=200))
    #print(content)
    date = check_date(_schmalkanden_st.search(content).group(1), "Schmalkanden")
    c = force_int(_schmalkanden_c.search(content).group(1))
    cc = force_int(_schmalkanden_cc.search(content).group(1))
    d = force_int(_schmalkanden_d.search(content).group(1))
    s = force_int(_schmalkanden_s1.search(content).group(1)) + force_int(_schmalkanden_s2.search(content).group(1))
    update(sheets, 16066, c=c, cc=cc, d=d, s=s, ignore_delta=True)
    return True

schedule.append(Task(11, 35, 14, 57, 600, schmalkanden, 16066))
if __name__ == '__main__': schmalkanden(googlesheets())
