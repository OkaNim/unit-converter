# import
import sys, re
import src_001_basic_221017 as src_001
import src_002_value_clean_230328 as src_002
import src_199_unit_recognizer_230324 as src_199
PRE_DATA = src_199.prepare_necessary_data()




# main
def main(ccu_file, value, texts):

    # Output component_units.
    output_component_unit(PRE_DATA)                                            # f


    if type(value) is not str: value = str(value)
    prop = ccu_file[:-len("_CCU.txt")]
    texts.append(value)



    # Recognize a unit.
    power_10_2, power_match_2, power_10_2_sign, i2 = '0', '_', 0, -1
    for i, text in enumerate(texts):
        if text == '_': continue
        unit_match, factor, calc, d_unit, power_10_2_sign = src_199.main(PRE_DATA, prop, text)    # i
        if unit_match != "_":
            i2 = i
            break
    if i2 == len(texts) - 1:
        value = delete_unit_in_value(unit_match, value)                        # f



    # Recognize power_10 in other than value.
    power_10_2, power_10_2_match = '0', '_'
    if i2 < len(texts) - 1:
        if i2 == -1: i2 = 0
        text = texts[i2]
        power_10_2, power_10_2_match = recognize_power_10_in_other_than_value(text, unit_match)    # f

        if i2 != 0 and power_10_2_match == '_':
            power_10_2, power_10_2_match = recognize_power_10_in_other_than_value(texts[0], unit_match)    # f



    # Clean a value.
    value_cl, power_10, _, power_10_match = src_002.main(value, in_value=1)    # i
    if src_002.is_float(value_cl):
        value_cl = float(value_cl)
        if power_10_2_match == "log": value_cl = 10**value_cl
        if power_10_2 != '0':
            power_10_2_int = int(power_10_2)
            if power_10_2_sign == 1: power_10_2_int = abs(power_10_2_int)
            elif power_10_2_sign == 2: power_10_2_int = abs(power_10_2_int) * -1
            value_cl *= 10**int(power_10_2_int)
        value_cl = str(value_cl)



    # Convert a value.
    if src_002.is_float(value_cl):
        if factor != "_":
            value_cv = convert_value(value_cl, factor, calc)                   # f
        else:
            value_cv = value_cl
        value_cl = "{:E}".format(float(value_cl))
        value_cv = "{:E}".format(float(value_cv))
    else:
        value_cv = ""



    # Edit results.
    if factor != "_": factor = "{:E}".format(factor)

    power_10, use_power_10 = "_", "use as recognized"
    if not power_10_match in ['_', '0']: power_10 = power_10_match + " (in value)"
    elif not power_10_2_match in ['_', '0']: power_10 = power_10_2_match

    if power_10_2_sign == 0: use_power_10 = "use as recognized"
    elif power_10_2_sign == 1: use_power_10 = "use as always positive"
    elif power_10_2_sign == 2: use_power_10 = "use as always negative"


    results = {
        "power_10":power_10,
        "value_cl":value_cl,
        "unit":unit_match,
        "value_cv":value_cv,
        "unit_cv":d_unit,
        "factor":factor,
        "use_power_10":use_power_10,
        "CCU_file":ccu_file,
        }


    return results




# f
def output_component_unit(PRE_DATA):
    COMP_UNIT = PRE_DATA[2]

    OUTPUT = [["symbol", "name"], [""]]    # , "factor", "destination"]]
    for i, name in enumerate(COMP_UNIT.keys()):
        for symbol in COMP_UNIT[name].keys():
            # factor = COMP_UNIT[name][symbol]["factor"]
            # destination = COMP_UNIT[name][symbol]["d_unit"]
            OUTPUT.append([symbol, name])    # , factor, destination])

    outdir = "./199_file"
    outfname = "used-comp-unit.dat"
    src_001.output(outdir + '/' + outfname, OUTPUT, sep="\t")                  # i



def delete_unit_in_value(unit_match, value):
    value = value.replace(unit_match, "")
    value = value.rstrip()
    value = value.lstrip()

    return value



def recognize_power_10_in_other_than_value(text, unit_match):
    power_10, match, match_2 = src_002.recognize_power_10(text, in_value=0)[1:]    # i
    if unit_match.lower() == "barrer" and int(power_10) <= -10: power_10, match, match_2 = '0', '_', '_'

    if not match in ['_', 'log']:
        inverse = check_sign_power_10(text, unit_match, power_10, match)       # f
        if inverse == 1:
            if power_10.startswith("-"): power_10 = power_10[1:]
            else: power_10 = "-" + power_10
            match_2 += " (need to inverse)"


    return power_10, match_2



def check_sign_power_10(text, unit_match, power_10, match):
    inverse = 0

    text = text.replace("x", "×")

    META_CHAR = ["\.", "\[", "\]", "\-", "\^", "\$", "\*" "\+", "\?", "\{", "\}", "\(", "\)"]
    for meta in META_CHAR:
        match = match.replace(meta[1], meta)
        unit_match = unit_match.replace(meta[1], meta)
    x = match + "[\s]?" + unit_match
    x = match + "[\s×·*.•]?" + unit_match
    pat = re.compile(r"%s"% x)
    m = pat.search(text)
    if not m: inverse = 1


    return inverse



def convert_value(value, factor, calc):
    value = float(value)
    if calc == '+': value += factor
    else: value *= factor

    return str(value)


