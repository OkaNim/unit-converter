# -*- coding: utf-8 -*-

def main():
    import sys
    import src_002_value_clean_211028 as src_2


    infname_data, infname_list = sys.argv[1], sys.argv[2]



    # Input a unit list
    INPUT = input_data(infname_list, tab=0, blanc_line=1)                                                      # def
    UNIT_LIST, calculation, power_of_10_method = edit_input(INPUT)                                             # def
    UNIT_GENE, COEFF_GENE = genecoeff_unit(UNIT_LIST)                                                          # def



    # Unit conversion
    INPUT = input_data(infname_data, tab=1, blanc_line=1)                                                      # import
    if len(INPUT[-1]) > 11: eval = 1
    else:
        eval = 0
        # INPUT.insert(1, ["INPUT"])
    HEADER, DATA = INPUT[:3], INPUT[3:]



    RESULT = []
    for i, x in enumerate(DATA):
        # if i > 1: break
        prop_specifier, value, related_tcd, tcaption, tfoot = x[3], x[4], x[8], x[9], x[10]

        # Recognize a unit
        place, power_of_ten_2, power_recognized_2 = "_", "_", "_"
        TEXT = [prop_specifier, related_tcd, tfoot, tcaption, value]
        PLACE = ["prop-specifier", "related-tcd", "tfootnote", "tcaption", "value"]
        for j, y in enumerate(TEXT):
            UNIT, COEFF, recog_unit = recognize_unit(y, UNIT_GENE, COEFF_GENE, calculation)                    # def
            if recog_unit == 1:
                place = PLACE[j]
                if j == 4: break
                power_of_ten_2, power_recognized_2, text = src_2.recognize_power_of_ten(y, prop=1)             # import
                if power_of_ten_2 != "_":
                    power_of_ten_2, power_recognized_2 = check_sign_power_of_ten(y, UNIT, power_of_ten_2, power_recognized_2)    # def
                if UNIT[0].lower() == "barrer" and power_of_ten_2 == "-10": power_of_ten_2, power_recognized_2 = "_", "_"
                break


        # Cleanse a value
        if place == "value":
            for y in UNIT: value = value.replace(y, "")
            value = value.rstrip()
            value = value.lstrip()
        value_clean, power_of_ten, power_recognized = src_2.clean_value(value)                                 # import
        log_recognized, value_clean = recognize_log(prop_specifier, value_clean, src_2)                        # def
        if power_recognized_2 == "_" and log_recognized == "log": power_recognized_2 = "log"

        # Convert a value
        for y in [power_of_ten, power_of_ten_2]:
            if power_of_10_method == 1:    # Always positive.
                if y.startswith("-"): y = y[1:]
            elif power_of_10_method == 2:    # Always negative. e.g. for gas permeability coefficient.
                if not y.startswith("-"): y = "-" + y
            if src_2.is_float(value_clean) and src_2.is_float(y): value_clean = str(float(value_clean) * 10**int(y))
        value_convert = value_clean
        value_convert = convert_unit(src_2, value_clean, COEFF, calculation)                                   # def

        # Edit for output
        value_clean = decimal_point_str_format(src_2, value_clean)                                             # def
        value_convert = decimal_point_str_format(src_2, value_convert)                                         # def
        for a in range(len(COEFF)):
            COEFF[a] = decimal_point_str_format(src_2, COEFF[a])                                               # def
        coeff = "  ×  ".join(COEFF)
        unit = "  +  ".join(UNIT)
        power = "  /  ".join([power_recognized, power_recognized_2])

        RESULT.append([power, unit, coeff, place, value_clean, value_convert])



    # Evaluation
    if eval == 1:
        PRED_POWER = list(map(lambda x: x[-6], RESULT))
        PRED_UNIT = list(map(lambda x: x[-5], RESULT))
        PRED_VALUE_CLEAN = list(map(lambda x: x[-2], RESULT))
        PRED_VALUE_CONVERT = list(map(lambda x: x[-1], RESULT))

        CA_POWER = list(map(lambda x: x[-6], DATA))
        CA_UNIT = list(map(lambda x: x[-5], DATA))
        CA_VALUE_CLEAN = list(map(lambda x: x[-2], DATA))
        CA_VALUE_CONVERT = list(map(lambda x: x[-1], DATA))

        EVAL_POWER = evaluation_1(PRED_POWER, CA_POWER)                                                        # def
        EVAL_UNIT = evaluation_1(PRED_UNIT, CA_UNIT)                                                           # def
        EVAL_VALUE_CLEAN = evaluation_2(src_2, PRED_VALUE_CLEAN, CA_VALUE_CLEAN)                               # def
        EVAL_VALUE_CONVERT = evaluation_2(src_2, PRED_VALUE_CONVERT, CA_VALUE_CONVERT)                         # def

        SCORE = []
        for i, x in enumerate([EVAL_POWER, EVAL_UNIT, EVAL_VALUE_CLEAN, EVAL_VALUE_CONVERT]):
            accuracy = sum(x) / len(x)
            accuracy = "{:.3f}".format(accuracy)
            if i == 0: word = "accuracy_power-of-ten-recognition"
            elif i == 1: word = "accuracy_unit-recognition"
            elif i == 2: word = "accuracy_value-cleansing"
            elif i == 3: word = "accuracy_unit-conversion"
            SCORE.append([word, "no-true", "no-false", "no-data", str(accuracy), str(sum(x)), str(len(x) - sum(x)), str(len(x))])

            for j, y in enumerate(x): RESULT[j].append(str(y))


        # Print screen
        print("")
        X = []
        for x in SCORE:
            result = " = ".join([x[0], x[4]]) + " (=" + "/".join([x[5], x[7]]) + ")"
            print(result)
            print("")
            X.append(result)
        HEADER[0].append(" / ".join(X))



    # Output
    for i, x in enumerate(DATA): x.extend(RESULT[i])
    OUTPUT = DATA

    if eval == 0:
        num_element = len(HEADER[1])
        for i in range(11 - num_element): HEADER[1].append("")
    HEADER[1].extend(["OUTPUT", "", "", "", "", ""])
    HEADER[2].extend(["power-of-ten-in-value/others", "unit", "coeff", "location-describing-unit", "value-clean", "value-convert"])


    if eval == 1:
        HEADER[1].extend(["EVALUATION", "", "", ""])
        HEADER[2].extend(["TF-power-of-ten", "TF-unit", "TF-value-clean", "TF-value-convert"])
    OUTPUT = edit_for_output(HEADER, OUTPUT)                                                       # def
    outfname = "OUT_conversion.dat"
    output(outfname, OUTPUT)                                                                       # def

    HEADER = [["unit", "coeff"]]
    OUTPUT = edit_for_output_2(HEADER, UNIT_GENE, COEFF_GENE)                                      # def
    outfname = "OUT_generated-unit.dat"
    output(outfname, OUTPUT)                                                                       # def



    # Print screen
    print("\n\nfinish\n\n")




# def
def edit_input(INPUT):
    import re

    calculation, power_of_10_method = 0, 0
    INPUT_2 = []
    start_1, start_2 = "_", "_"
    for x in INPUT:
        if x.startswith("#"): continue
        elif x.startswith("calculation"): calculation = int(x[-1])
        elif x.startswith("power_of_10"): power_of_10_method = int(x[-1])
        elif x.startswith("1st part"):
            x = x.split(", ")
            start_1 = x[0][-3:]
            order_non_fix_1 = int(x[1][-1])
        elif x.startswith("2nd part"):
            if not "start=(" in x: continue
            x = x.split(", ")
            start_2 = x[0][-3:]
            order_non_fix_2 = int(x[1][-1])
        else:
            if re.search(r"^\([0-9][0-9]?\)", x):
                if x.startswith(start_1): INPUT_2.append([order_non_fix_1])
                if x.startswith(start_2): INPUT_2.append([order_non_fix_2])
                INPUT_2[-1].append([[], []])
            else:
                if "\t" in x: x = x.split("\t")
                else: x = [x, "_"]
                x[0] = x[0].replace("999", "")
                INPUT_2[-1][-1][0].append(x[0])
                INPUT_2[-1][-1][1].append(x[1])

    return INPUT_2, calculation, power_of_10_method



def genecoeff_unit(INPUT):
    import itertools

    UNIT, COEFF = [], []
    for i in range(len(INPUT)):
        INTER_CHAR, UNIT_CONS, COEFF_CONS = [], [], []
        for j in range(len(INPUT[i])):
            if j == 0: order_non_fix = INPUT[i][j]
            else:
                if INPUT[i][j][1][0] == "_": INTER_CHAR = INPUT[i][j][0]
                else:
                    UNIT_CONS.append(INPUT[i][j][0])
                    COEFF_CONS.append(INPUT[i][j][1])
        if INTER_CHAR == []: INTER_CHAR = ["" for a in UNIT_CONS]

        UNIT_i = []
        p = itertools.product(*UNIT_CONS)
        for x in p:
            if order_non_fix == 1:
                q = itertools.permutations(x)
                for y in q:
                    for char in INTER_CHAR:
                        unit = char.join(y)
                        if unit[0] in INTER_CHAR: unit = unit[1:]
                        if unit[-1] in INTER_CHAR: unit = unit[:-1]
                        UNIT_i.append(unit)
            else:
                for char in INTER_CHAR:
                    unit = char.join(x)
                    if unit[0] in INTER_CHAR: unit = unit[1:]
                    if unit[-1] in INTER_CHAR: unit = unit[:-1]
                    UNIT_i.append(unit)

        COEFF_i = []
        p = itertools.product(*COEFF_CONS)
        for x in p:
            if order_non_fix == 1:
                q = itertools.permutations(x)
                for y in q:
                    for char in INTER_CHAR:
                        coeff = 1
                        for z in y: coeff *= float(z)
                        COEFF_i.append(coeff)
            else:
                for char in INTER_CHAR:
                    coeff = 1
                    for z in x: coeff *= float(z)
                    COEFF_i.append(coeff)

        UNIT_i_2, COEFF_i_2 = [], []        # Remove the same unit expression.
        for j, unit in enumerate(UNIT_i):
            if not unit in UNIT_i_2:
                UNIT_i_2.append(unit)
                COEFF_i_2.append(COEFF_i[j])

        UNIT.append(UNIT_i_2)
        COEFF.append(COEFF_i_2)

    return UNIT, COEFF



def check_sign_power_of_ten(text, UNIT, power_of_ten_2, power_recognized_2):
    import re

    pat = re.compile(r"%s"% power_recognized_2 + "\s?" + UNIT[0])
    m = pat.search(text)
    if not m:
        cnt_unit, cnt_power_of_ten = 0, 0
        for x in ["\([^\)]+\)", "\[[^\]]+\]"]:
            pat = re.compile(r"%s"% x)
            M = pat.findall(text)
            if M == [] or cnt_unit == 1: continue
            for m in M:
                for j, y in enumerate(UNIT):
                    if [j, y] == [1, "_"]: break
                    j2 = j + 1
                    if y in m: cnt_unit += 1
                cnt_unit = cnt_unit / j2
                if cnt_unit != 1: continue
                if power_recognized_2 in m: cnt_power_of_ten = 1
                break

        if cnt_unit == 1 and cnt_power_of_ten == 0:
            if power_of_ten_2.startswith("-"): power_of_ten_2 = power_of_ten_2[1:]
            else: power_of_ten_2 = "-" + power_of_ten_2
            power_recognized_2 += " (i)"

    return power_of_ten_2, power_recognized_2



def recognize_log(text, value_clean, src_2):
    log_recognized = "_"
    if "log" in text:
        adopt_recog = adopt_recognition("log", text)                                                          # def
        if adopt_recog == 1:
            if src_2.is_float(value_clean):
                log_recognized = "log"
                value_clean = str(10**float(value_clean))

    return log_recognized, value_clean



def adopt_recognition(recog, text):
    import re

    adopt_recog, a1, a3 = 0, 0, 0
    while adopt_recog == 0 and a1 > -1:
        a1 = text.find(recog, a3)
        if a1 > -1:
            a3 = a1 + 1
            adopt_recog = 1
            if len(recog) <= 3:
                if a1 > 0:
                    if re.search(r"[a-zA-Z]", text[a1 - 1]): adopt_recog = 0
                if adopt_recog == 1:
                    a2 = a1 + len(recog)
                    if a2 + 1 <= len(text):
                        if re.search(r"[a-zA-Z]", text[a2]): adopt_recog = 0

    return adopt_recog



def recognize_unit(text, UNIT_GENE, COEFF_GENE, calculation):
    import re

    UNIT = ["_" for a in UNIT_GENE]
    if calculation == 1: COEFF = [0 for a in UNIT_GENE]
    else: COEFF = [1 for a in UNIT_GENE]

    recog_unit = 0
    for i in range(len(UNIT_GENE)):
        if "Barrer" in UNIT or "barrer" in UNIT: break
        for j, unit_gene in enumerate(UNIT_GENE[i]):
            if "Barrer" in UNIT or "barrer" in UNIT: break
            coeff_gene = COEFF_GENE[i][j]
            if unit_gene in text:
                unit_gene = unit_gene.rstrip()        # Ocassionally, unit_gene[-1] == " " (whitespace).

                adopt_recog = adopt_recognition(unit_gene, text)                                              # def
                if adopt_recog == 0: continue

                if UNIT[i] == "_":
                    UNIT[i], COEFF[i] = unit_gene, coeff_gene
                    recog_unit = 1
                else:
                    if len(unit_gene) > len(UNIT[i]): UNIT[i], COEFF[i] = unit_gene, coeff_gene    # Longer unit is adopted.
        if len(UNIT) > 1:
            if UNIT[0] != "_": text = text.replace(UNIT[0], "")


    return UNIT, COEFF, recog_unit



def convert_unit(src_2, value, COEFF, calculation):
    if src_2.is_float(value):
        value = float(value)
        for coeff in COEFF:
            if calculation == 1: value += coeff
            else: value *= coeff

    return str(value)



def decimal_point_str_format(src_2, value):
    from decimal import Decimal

    if type(value) != str: value = str(value)
    if not value.isdigit() and src_2.is_float(value):
        if len(str(value)) > 6: value = str("{:.5E}".format(float(value)))
        value = "{}".format(Decimal.normalize(Decimal(value)))

    return value



def evaluation_1(PRED, CA):
    EVAL = [0 for a in PRED]
    for i, x in enumerate(PRED):
        pred, ca = x, CA[i]
        if pred == ca: EVAL[i] = 1

    return EVAL



def evaluation_2(src_2, PRED, CA):
    EVAL = [0 for a in PRED]
    for i, x in enumerate(PRED):
        if not src_2.is_float(x): continue
        pred, ca = float(x), float(CA[i])
        if ca == 0:
            if abs(pred - ca) < 1e-4: EVAL[i] = 1
        else:
            if abs(pred/ca - 1) < 1e-4: EVAL[i] = 1

    return EVAL



def edit_for_output_2(HEADER, UNIT_GENE, COEFF_GENE):
    OUTPUT_2 = []
    for x in HEADER: OUTPUT_2.append("\t".join(x))
    for i, x in enumerate(UNIT_GENE):
        for j, y in enumerate(x):
            unit, coeff = y, str(COEFF_GENE[i][j])
            OUTPUT_2.append("\t".join([unit, coeff]))
        OUTPUT_2.append("")
    del OUTPUT_2[-1]

    return OUTPUT_2



def input_data(infname, tab, blanc_line):
    with open(infname, "r", encoding = "utf-8") as inf:
        INPUT = []
        for x in inf:
            x = x[:-1]
            if blanc_line == 1 and x == "": continue
            if tab == 1: x = x.split("\t")
            INPUT.append(x)

    return INPUT



def edit_for_output(HEADER, OUTPUT):
    OUTPUT_2 = []
    for x in HEADER: OUTPUT_2.append("\t".join(x))
    for i, x in enumerate(OUTPUT): OUTPUT_2.append("\t".join(x))

    return OUTPUT_2



def output(outfname, OUTPUT):
    with open(outfname, "w", encoding = "utf-8") as outf:
        for x in OUTPUT: print(x, file = outf)




# Main
if __name__ == "__main__": main()


