#!/usr/bin/python3
from botbase import *

_offenbach_c = re.compile(r"Insgesamt wurden bislang ([0-9.]+)\sMenschen in Offenbach positiv")
_offenbach_d = re.compile(r"Todesfälle in Offenbach gab es bisher insgesamt ([0-9.]+)\.")
_offenbach_g = re.compile(r"([0-9.]+ )Menschen sind inzwischen wieder genesen")
_offenbach_si = re.compile(r"Es werden derzeit\s+(\S+)\s+Person(?:en)? aus Offenbach im Krankenhaus behandelt(?:, bei\s+(\S+)\s+Person(?:en)? ist der Zustand kritisch)?")

def offenbach(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.offenbach.de/leben-in-of/gesundheit/stadtgesundheit/corona/coronavirus_meldungen.php")
    main = soup.find(id="SP-content")
    text = re.sub(r"\s*\n\s*","\n",main.get_text(" ").strip())
    #print(text)
    if not today().strftime("Stand: %-d. %B %Y") in text: raise NotYetAvailableException("Offenbach noch alt.")
    c = force_int(_offenbach_c.search(text).group(1))
    d = force_int(_offenbach_d.search(text).group(1))
    g = force_int(_offenbach_g.search(text).group(1)) if _offenbach_g.search(text) else None
    s, i = map(force_int, _offenbach_si.search(text).groups()) if _offenbach_si.search(text) else (None, None)
    comment = "Bot" if s is not None else "Bot ohne SI"
    update(sheets, 6413, c=c, g=g, d=d, s=s, i=i, sig="Bot", comment=comment)
    return True

schedule.append(Task(10, 0, 14, 35, 360, offenbach, 6413))
if __name__ == '__main__': offenbach(googlesheets())
