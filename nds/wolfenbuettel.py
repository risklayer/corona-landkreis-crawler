#!/usr/bin/python3
from botbase import *

_wolfenbuettel_c = re.compile(r"sind ([0-9.]+) \(([+-]?[0-9.]+)\) Fälle nachgewiesen")
_wolfenbuettel_d = re.compile(r"([0-9.]+) \(([+-]?[0-9.]+)\) Personen, bei denen [^.,0-9]*, sind verstorben")
_wolfenbuettel_g = re.compile(r"([0-9.]+) \(([+-]?[0-9.]+)\) Personen wieder genesen")

def wolfenbuettel(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.lkwf.de/Aktuelles/Presse/Informationen-des-Landkreises-zum-Corona-Virus.php?object=tx,3282.5.1&ModID=7&FID=3282.10903.1&NavID=175.225&La=1&kat=175.7%2C2697.106")
    main = soup.find("article").find(class_="inner")
    text = main.get_text(" ").strip()
    #print(text)
    if not today().strftime("Stand %-d. %B %Y") in text: raise NotYetAvailableException("Wolfenbüttel noch alt")
    args=dict()
    args["c"], args["cc"] = map(force_int, _wolfenbuettel_c.search(text).groups())
    args["d"], args["dd"] = map(force_int, _wolfenbuettel_d.search(text).groups())
    args["g"], args["gg"] = map(force_int, _wolfenbuettel_g.search(text).groups())
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 3158, **args, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(11, 30, 14, 35, 600, wolfenbuettel, 3158))
if __name__ == '__main__': wolfenbuettel(googlesheets())
