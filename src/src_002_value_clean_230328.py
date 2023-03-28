# import
import re




# main
def main(text, in_value):
    text = unify_char(text)                                                    # f

    text, power_10, match, match_2 = recognize_power_10(text, in_value)        # f

    if match == '_':
        text, power_10, match = recognize_kilo(text)                           # f

    if not is_float(text):
        text = select_one_value_with_1000sep(text)                             # f

    if not is_float(text):
        text = select_one_value(text)                                          # f

    if is_float(text):
        if in_value == 1 and power_10 != '0':
            text = float(text) * 10**int(power_10)
            text = str(text)
    else:
        text = "Not a number"


    return text, power_10, match, match_2




# f
def is_float(text):
    try:
        float(text)
    except:
        return False
    return True



def unify_char(text):
    text = text.replace("–", "-")
    text = text.replace("−", "-")
    text = text.replace("x", "×")

    return text



def recognize_power_10(text, in_value):
    power_10, match, match_2 = '0', '_', '_'

    rexp = "(.?)(10|[Ee])(\s?)(-?[0-9]+)"
    # rexp = "([×·*]?\s?)(10|[Ee])(\s?)(-?[0-9]+)"
    pat = re.compile(r"%s" % rexp)
    m = pat.search(text)
    m2 = 0
    if m:
        if not re.search(r"[A-Za-zΑ-Ωα-ω]+", m.groups()[0]): m2 = 1
        # if m.groups()[0] in ['×', '·', '*', ' ']
    if m2 == 1:
        match = "".join(m.groups()[1:])
        power_10 = m.groups()[-1]

        if abs(int(power_10)) > 50: power_10, match = '0', '_'
        elif int(power_10) == 0: power_10, match = '0', '_'
        elif int(power_10) == 1:
            if m.groups()[0] in ["", ' ']: power_10, match = '0', '_'

        if in_value == 1:
            if re.search(r"^10[0-9]+", match): power_10, match = '0', '_'    # e.g. "1017" is not a power of ten in value mostly.
            elif re.fullmatch(r"[,\s\.]100", match): power_10, match = '0', '_'    # e.g. "100" is incorrectly matched in "38 100".

        if match != '_': match_2 = "".join(m.groups()[1:])

        if in_value == 1 and match != '_':
            if text.startswith(match_2):    # Eg, "10-2 @ 5 wt %", "10-4"
                text = str(10**int(power_10))
                power_10 = '0'
            else:
                text = text.replace(match, "")
                text = text.rstrip()
                text = text.lstrip()

            if text == "": text = '1'
            elif len(text) == 1 and not re.search(r"[0-9]", text): text = '1'


    if in_value == 0 and match == '_':
        match = recognize_log(text)                                            # f
        if match == "log": match_2 = "log"


    match = match.rstrip()
    match = match.lstrip()


    return text, power_10, match, match_2



def recognize_log(text):
    match = '_'

    pat = re.compile(r"%s" % "(.?)(log)(.?)")
    m = pat.search(text)
    if m:
        judge = 1
        for x in m.groups()[::2]:
            if re.search(r"[Α-ωA-Za-z]", x):
                judge = 0
                break

        if judge == 1: match = "log"


    return match



def recognize_kilo(text):
    power_10, match = '0', '_'

    rexp = "([0-9]+)(\s*)([kK]$)"
    pat = re.compile(rexp)
    m = pat.search(text)
    if m:
        if is_float(m.groups[0]):
            match = m.groups()[2]
            power_10 = '3'
            text = m.groups[0]


    return text, power_10, match



def select_one_value_with_1000sep(text):
    m = re.search(r"(-?[0-9]{1,3}[,\s]?)+(\.[0-9]+)?", text)
    if m:
        text = m.group()
        text = text.rstrip()
        if "," in text or " " in text:
            if re.fullmatch(r"-?[1-9][0-9]{0,2}([,\s][0-9]{3})+(\.[0-9]+)?", text): text = text.replace(",", "").replace(" ", "")    # Remove thousand separators.

    return text



def select_one_value(text):
    m = re.search(r"-?[0-9]+(\.[0-9]+)?", text)
    if m:
        text = m.group()

    return text


