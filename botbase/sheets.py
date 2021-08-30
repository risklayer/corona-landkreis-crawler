import sys, re
# Spreadsheet ID we are using
spreadsheet_id = '1wg-s4_Lz2Stil6spQEYFdZaBEp8nWW26gVyfHqvcl8s'

# Global command line "dry run" parameter
dry_run="--dry-run" in sys.argv

from .parse import * # force_int

_namemap=None
def ags_from_name(nam):
    global _namemap
    if not _namemap:
        _namemap = dict()
        for line in open("namemap.csv"):
            a, n = line.strip().split("\t")
            _namemap[n] = int(a)
    return _namemap.get(nam)

_agsmap=None
def get_ags(sheets):
    global _agsmap
    if _agsmap: return _agsmap
    result = sheets.values().get(spreadsheetId=spreadsheet_id, range="Haupt!C6:C406").execute()
    values = result.get('values', [])
    _agsmap=dict()
    for i, row in enumerate(values):
        _agsmap[int(row[0])] = i + 6
    return _agsmap

def is_signed(sheets, ags):
    """Check if a row is already signed. We need to sleep a bit here, to avoid triggering Google rate limits."""
    ags = int(ags)
    rownr = get_ags(sheets)[ags]
    if not rownr: raise Exception("AGS '%s' not found" % ags)
    import time
    time.sleep(.5)
    result = sheets.values().get(spreadsheetId=spreadsheet_id, range="Haupt!S%d" % rownr).execute()
    values = result.get('values', [])
    if not values: return None # empty, this is okay.
    v = values[0][0]
    if v is None or v == "" or v.lower() == "vorläufig" or v == "nn": return None
    return v

def set_one(sheets, cell, value, dry_run=dry_run):
    """Unfortunately, not very fast"""
    if dry_run:
        print("Update", cell, value)
        return
    sheets.values().update(spreadsheetId=spreadsheet_id, range=cell, valueInputOption="RAW", body = {"values":[[value]]}).execute()

def _format(c, v, vv=None):
    if v is None: return None
    if vv is None: return "%s%d" % (c,v)
    return ("%s%d(%+d)" % (c,v,vv)) if vv != 0 else ("%s%d(=)" % (c,v))

_stripbot=re.compile(r"\(?Bot.*(?: [A-Z][0-9]+[()0-9=]+)+\)?")

def update(sheets, ags, c, cc=None, d=None, dd=None, g=None, gg=None, q=None, s=None, i=None, sig="Bot", comment=None, dry_run=dry_run, date=None, check=None, ignore_delta=False, batch=None, without_c=False):
    import datetime
    if date is None:
        date = datetime.date.today().strftime("%d.%m.%Y")
    elif isinstance(date, datetime.datetime):
        date = date.strftime("%d.%m.%Y %H:%M").replace(" 00:00","")
    elif isinstance(date, datetime.date):
        date = date.strftime("%d.%m.%Y")
    strs = [_format("C",c,cc), _format("D",d,dd), _format("G",g,gg), _format("Q",q), _format("S",s), _format("I",i)]
    rownr = get_ags(sheets)[ags]
    if not rownr: raise Exception("AGS '%s' not found" % ags)
    curr = sheets.values().get(spreadsheetId=spreadsheet_id, range="Haupt!D%d:AN" % rownr, valueRenderOption="UNFORMATTED_VALUE").execute()
    row = curr.get('values', [])[0]
    check = True if check is None else check(row[14]) and True
    if row[15] is not None and row[15] not in ["", "nn", "RKI", "Vorläufig"]:
        comment = (comment if comment else sig) + " " + " ".join([x for x in strs if x is not None])
        print("Skipping:", ags, rownr, comment, "is already:", row[15])
        return # already filled!
    #if not check and row[15] == "Vorläufig": return
    if not check: sig = "Vorläufig"
    comment = (comment if comment else sig) + " " + " ".join([x for x in strs if x is not None])
    print(ags, row[15], "->", comment)

    prev = int(row[0]), int(row[-2]), int(row[-1])
    do_apply = True
    if not without_c and not ignore_delta and cc is not None and prev[0] != c - cc:
        print("Previous C value does not match: %d vs. %d" % (prev[0], c - cc))
        do_apply = False
    if not ignore_delta and dd is not None and prev[2] != d - dd:
        print("Previous D value does not match: %d vs. %d" % (prev[2], d - dd))
        do_apply = False
    if not ignore_delta and gg is not None and prev[1] != g - gg:
        print("Previous G value does not match: %d vs. %d" % (prev[1], g - gg))
        do_apply = False
    #if not without_c and do_apply and cc is None and c < int(row[0]): do_apply = False
    if sig in row[17]: return # schon von Bot kommentiert
    if do_apply:
        reqs = list()
        if c != int(prev[0]) and c != int(row[7]):
            reqs.append({"range": "Haupt!K%d" % rownr, "values": [[c]]})
        #elif c is not None: comment=comment.replace(strs[0], "(%s)" % strs[0])
        if d is not None and d != int(prev[2]) and d != force_int(row[12]):
            reqs.append({"range": "Haupt!P%d" % rownr, "values": [[d]]})
        #elif d is not None: comment=comment.replace(strs[1], "(%s)" % strs[1])
        if g is not None and g != int(prev[1]) and g != force_int(row[8]):
            reqs.append({"range": "Haupt!L%d" % rownr, "values": [[g]]})
        #elif g is not None: comment=comment.replace(strs[2], "(%s)" % strs[2])
        if q is not None and q != force_int(row[9]): reqs.append({"range": "Haupt!M%d" % rownr, "values": [[q]]})
        if s is not None and s != force_int(row[10]): reqs.append({"range": "Haupt!N%d" % rownr, "values": [[s]]})
        if i is not None and i != force_int(row[11]): reqs.append({"range": "Haupt!O%d" % rownr, "values": [[i]]})
        #if len(reqs) == 0: return
        #comment=comment.replace(")) (", ") ")
        reqs.append({"range": "Haupt!Q%d" % rownr, "values":[[date]]})
        reqs.append({"range": "Haupt!S%d" % rownr, "values":[[sig]]})
        v = comment + " " + _stripbot.sub("",row[17]) if row[17] is not None and row[17] != "" and not row[17].startswith("Zwischenstand") else comment
        reqs.append({"range": "Haupt!U%d" % rownr, "values":[[v]]})
        if dry_run:
            print(*reqs, sep="\n")
            return
        if batch is not None:
            batch.extend(reqs)
        else:
            do_batch(sheets, reqs)
        return
    if do_apply or row[17] is None or row[17] == "": # or row is RKI pattern!
        v = comment + " " + _stripbot.sub("",row[17]) if row[17] is not None and row[17] != "" else comment
        if batch is not None:
            batch.append({"range":"Haupt!U%d" % rownr, "values":[["("+v+")"]]})
            return
        set_one(sheets, "Haupt!U%d" % rownr, "("+v+")", dry_run=dry_run) # Comment

def do_batch(sheets, reqs, dry_run=dry_run):
    if dry_run:
        print(*reqs, sep="\n")
        return
    if len(reqs) == 0: return
    #print(*reqs, sep="\n")
    responses = sheets.values().batchUpdate(spreadsheetId=spreadsheet_id, body = {"valueInputOption":"USER_ENTERED", "data":reqs}).execute()
    if not "responses" in responses: print(responses)
    for resp in responses["responses"]:
        if resp.get("updatedCells") != 1: print("Failed?", resp, file=sys.stderr)
