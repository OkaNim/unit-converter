# -*- coding: utf-8 -*-

def clean_value(text):
    import re

    text = change_char_style(text)                                                                  # def

    power_of_ten, recognized, text = recognize_power_of_ten(text, prop=0)                           # def
    if power_of_ten == "_":
        power_of_ten, recognized = recognize_kilo(text)                                             # def
    if power_of_ten != "_":
        text = text.replace(recognized, "")
        if text == "": text = "1"
        elif len(text) == 1 and not re.search(r"[0-9]", text): text = "1"

    if not is_float(text):
        text = select_one_value(re, text)                                                           # def

    if not is_float(text):
        text = select_one_value_2(re, text)                                                         # def

    if not is_float(text): text = "NaN"


    return text, power_of_ten, recognized




# def
def is_float(text):
    try:
        float(text)
    except:
        return False
    return True



def change_char_style(text):
    text = text.replace("–", "-")        # minus (ACS)
    text = text.replace("−", "-")        # minus (ELSEVIER)
    text = text.replace("x", "×")

    return text



def recognize_power_of_ten(text, prop):
    import re

    POWER_OF_TEN = ["[Ee]\s?-?[0-9][0-9]*", "[×·*]?\s?10\s?-?[1-9][0-9]*"]
    if prop == 1: POWER_OF_TEN = ["10\s?-?[1-9][0-9]*"]

    power_of_ten, recognized = "_", "_"
    for a in POWER_OF_TEN:
        pat = re.compile(r"%s" % a)
        m = pat.search(text)
        if m:
            if m.group() in ["e1", "E1"]: continue    # Assuming that "e1" and "E1" are not generally used.
            if prop == 0 and re.search(r"^10[0-9]", m.group()): continue    # e.g. "1017", which is not a power of ten in value.
            if prop == 0 and re.search(r"^10-[0-9]", m.group()):    # No a value before a power of ten, e.g. "10-2 @ 5 wt %".
                if text.startswith(m.group()):
                    power_of_ten, recognized = m.group()[2:], m.group()
                    text = str(10**int(power_of_ten))
                    power_of_ten = "0"
                    break
            recognized = m.group()
            if "E" in a.upper(): a = a.replace("-?[0-9][0-9]*", "")
            else: a = a.replace("-?[1-9][0-9]*", "")
            pat_2 = re.compile(r"^%s" % a)
            power_of_ten = pat_2.sub("", recognized)
            n = re.search(r"^-?0", power_of_ten)    # In the case of 'E-09'
            if n:
                modify = n.group().replace("0", "")
                power_of_ten = modify + power_of_ten[len(n.group()):]
            break

    if [power_of_ten, recognized] != ["_", "_"]:
        if is_float(power_of_ten):
            if abs(int(power_of_ten)) > 50: power_of_ten, recognized = "_", "_"
        else: power_of_ten, recognized = "_", "_"


    return power_of_ten, recognized, text



def recognize_kilo(text):
    import re

    power_of_ten, recognized = "_", "_"

    pat = re.compile(r"\s*[k, K]$")
    m = pat.search(text)
    if m:
        x = pat.sub("", text)
        if is_float(x):
            recognized = m.group()
            power_of_ten = "3"

    return power_of_ten, recognized



def select_one_value(re, text):
    m = re.search(r"(-?[0-9]{1,3}[,\s]?)+(\.[0-9]+)?", text)
    if m:
        text = m.group()
        text = text.rstrip()
        if "," in text or " " in text:
            if re.fullmatch(r"-?[1-9][0-9]{0,2}([,\s][0-9]{3})+(\.[0-9]+)?", text): text = text.replace(",", "").replace(" ", "")    # Remove thousand separators.

    return text



def select_one_value_2(re, text):
    m = re.search(r"-?[0-9]+(\.[0-9]+)?", text)
    if m:
        text = m.group()
        text = text.rstrip()
        text = text.lstrip()

    return text


