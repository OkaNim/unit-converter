# import
import sys, re, itertools, math, copy
from fractions import Fraction
import src_001_basic_221017 as src_001




# main
def main(PRE_DATA, prop, text):
    OK_TEXT, EQ_ALL, COMP_UNIT = PRE_DATA

    value_2, match, factor_2 = '_', '_', '_'

    calc, d_unit, power10_sign = '*', '_', 0
    if prop in EQ_ALL.keys():
        if len(EQ_ALL[prop]["eq"]) == 1 and EQ_ALL[prop]["eq"][0][0] == "*temperature": calc = '+'

        PAT, d_factor, d_unit, power10_sign = generate_unit_notation(COMP_UNIT, EQ_ALL, prop, text)    # f

        judge, match, factor, d_factor = recognize_unit(OK_TEXT, PAT, d_factor, text)    # f
        if judge == 1:
            if calc == '*': factor_2 = factor / d_factor
            elif calc == '+': factor_2 = factor - d_factor


    return match, factor_2, calc, d_unit, power10_sign




# f
def prepare_necessary_data():
    OK_TEXT = import_allowable_char()                                          # f


    EQ_ALL = import_unit_eqaution()                                            # f
    # for x in EQ_ALL.items(): print("EQ ", x, "\n")
    # for y in x: print(y, "\n")


    COMP_UNIT = import_component_unit(EQ_ALL)                                  # f
    # print("\n", COMP_UNIT)


    return OK_TEXT, EQ_ALL, COMP_UNIT



def import_allowable_char():
    infname = "./199_file/other-necessaries/allowable-char.txt"
    INPUT = src_001.input_data(infname, tab=0, blanc_line=1)                   # i
    OK_TEXT = INPUT[1:]
    OK_TEXT.append("")
    OK_TEXT.append(' ')
    for i in range(10): OK_TEXT.append(str(i))

    return OK_TEXT



def import_unit_eqaution():
    indir = "./199_file/CCU"
    INFNAME = src_001.file_list(indir, EXT=["_CCU.txt"])                       # i

    EQ_ALL_2 = {}
    for i, infname in enumerate(INFNAME):
        # print("\n", i + 1, "\t", infname)

        INPUT = src_001.input_data(indir + '/' + infname, tab=0, blanc_line=1)    # i

        eq, d_unit, sign = 0, "", 0
        INPUT_2 = []
        for i, x in enumerate(INPUT):
            if x.startswith('#'): continue
            if x.startswith("-- "):
                if x.startswith("-- combination"): eq = 1
                elif x.startswith("-- destination"): eq, d_unit = 0, INPUT[i + 1]
                elif x.startswith("-- + or - sign"): sign = int(INPUT[i + 1][-2])
            if eq == 1: INPUT_2.append(x)

        EQ_ALL = []
        for eq in INPUT_2[1:]:
            EQ = eq.split()
            start, stop = -1, -1
            for k, eq in enumerate(EQ):
                if '[' in eq:
                    EQ[k] = EQ[k][1:]
                    start = k
                if ']' in eq:
                    EQ[k] = EQ[k][:-1]
                    stop = k
            EQ.extend([start, stop])
            EQ_ALL.append(EQ)

        EQ_ALL_2[infname[:-len("_CCU.txt")]] = {"eq":EQ_ALL, "d_unit":d_unit, "power10_sign":sign}


    return EQ_ALL_2



def import_component_unit(EQ_ALL):
    infname = "./199_file/unit-prefix/unit-prefix.txt"
    INPUT = src_001.input_data(infname, tab=1, blanc_line=1)                   # i
    PREFIX = {a[2]: float(a[0]) for a in INPUT[1:]}


    indir = "./199_file/component-unit"
    INFNAME = src_001.file_list(indir, EXT=[".txt"])                           # i
    COMP_UNIT = {}
    for i, infname in enumerate(INFNAME):
        INPUT = src_001.input_data(indir + '/' + infname, tab=1, blanc_line=1)    # i
        X = {}
        for x in INPUT[1:]:
            symbol, d_unit, factor, pre_used = x[0], x[1], float(x[2]), x[3]
            if ':' in d_unit: d_category, d_unit = d_unit.split(": ")
            else: d_category = '_'

            if pre_used in ["non", '_']: PRE_USED = []
            elif pre_used == "all": PRE_USED = PREFIX.keys()
            else:
                PRE_USED = pre_used.split(",")
                for j in range(len(PRE_USED)): PRE_USED[j] = PRE_USED[j].replace(' ', "")
            X = add_dictionary(X, symbol, d_category, d_unit, factor, PRE_USED)    # f

            if PRE_USED != []:
                Y = add_prefix(PREFIX, symbol, d_category, d_unit, factor, PRE_USED)    # f
                X.update(Y)
        COMP_UNIT[infname[:-len(".txt")]] = X


    infname = "./199_file/other-necessaries/symbol-variant.txt"
    INPUT = src_001.input_data(infname, tab=1, blanc_line=1)                   # i
    for x in INPUT[1:]:
        symbol_variant, comp_unit, symbol = x

        y = COMP_UNIT[comp_unit][symbol]
        d_category, d_unit, factor, PRE_USED = y["d_category"], y["d_unit"], y["factor"], y["prefix_used"]

        X = {}
        X = add_dictionary(X, symbol_variant, d_category, d_unit, factor, PRE_USED)    # f

        if PRE_USED != ['_']:
            Y = add_prefix(PREFIX, symbol_variant, d_category, d_unit, factor, PRE_USED)    # f
            X.update(Y)

        COMP_UNIT[comp_unit].update(X)


    for comp_unit in COMP_UNIT.keys():
        for symbol in COMP_UNIT[comp_unit].keys():
            X = COMP_UNIT[comp_unit][symbol]
            d_category = X["d_category"]

            if d_category in COMP_UNIT.keys():
                d_unit = X["d_unit"]
                factor = COMP_UNIT[d_category][d_unit]["factor"]
                X["factor"] *= factor

            elif d_category in EQ_ALL.keys():
                d_unit = X["d_unit"]
                factor = calculate_factor_for_desitination(d_unit, COMP_UNIT)    # f
                X["factor"] *= factor


    return COMP_UNIT



def add_dictionary(X, symbol, d_category, d_unit, factor, PRE_USED):
    X[symbol] = {"d_category":d_category, "d_unit":d_unit, "factor":factor, "prefix_used":PRE_USED}

    return X



def add_prefix(PREFIX, symbol, d_category, d_unit, factor, PRE_USED):
    X = {}
    for pre in PRE_USED:
        symbol_2 = pre + symbol
        if symbol[-1].isnumeric(): power = int(symbol[-1])
        else: power = 1
        factor_2 = factor * (PREFIX[pre] ** power)

        X = add_dictionary(X, symbol_2, d_category, d_unit, factor_2, ['_'])    # f


    return X



def calculate_factor_for_desitination(d_unit, COMP_UNIT):
    D_UNIT = d_unit.split()
    X = []
    power = 1
    for symbol in D_UNIT:
        div = 0

        m = re.search(r"(^/|-[1-9]$)", symbol)
        if m:
            div = 1
            if m.group() in ['/', "-1"]: symbol = symbol.replace(m.group(), "")
            else: symbol = symbol.replace('-', "")

        m = re.search(r"-?[0-9]\.[0-9]+$", symbol)
        if m:
            if '-' in m.group(): div = 1
            power = abs(float(m.group()))
            symbol = symbol.replace(m.group(), "")

        for key in COMP_UNIT.keys():
            if symbol in COMP_UNIT[key].keys():
                if key in ["water-mass"]: continue
                factor = COMP_UNIT[key][symbol]["factor"]
                factor **= power
                if div == 1:
                    if key == "temperature": factor = 1
                    else: factor = 1/factor
                X.append(factor)
                break

    factor = math.prod(X)


    return factor



def generate_unit_notation(COMP_UNIT, EQ_ALL, prop, text):
    d_unit = EQ_ALL[prop]["d_unit"]
    power10_sign = EQ_ALL[prop]["power10_sign"]
    d_factor = calculate_factor_for_desitination(d_unit, COMP_UNIT)            # f

    PAT_2 = []
    for i, EQ in enumerate(EQ_ALL[prop]["eq"]):
        start, stop = EQ[-2:]

        j2 = 999
        for j, x in enumerate(EQ[:-2]):
            X, calc, j2 = gather_symbol_and_factor(x, COMP_UNIT, j, j2, text)    # f

            if j == 0: X1 = X
            elif j == 1: X2 = X
            elif j == 2: X3 = X
            elif j == 3: X4 = X
            elif j == 4: X5 = X


        if len(EQ[:-2]) == 1: P = itertools.product(X1)
        elif len(EQ[:-2]) == 2: P = itertools.product(X1, X2)
        elif len(EQ[:-2]) == 3: P = itertools.product(X1, X2, X3)
        elif len(EQ[:-2]) == 4: P = itertools.product(X1, X2, X3, X4)
        elif len(EQ[:-2]) == 5: P = itertools.product(X1, X2, X3, X4, X5)


        PAT = create_notation_pattern(P, calc, j2, start, stop)                # f
        PAT_2.extend(PAT)


    return PAT_2, d_factor, d_unit, power10_sign



def gather_symbol_and_factor(x, COMP_UNIT, i, i2, text):
    calc, comp_unit = x[0], x[1:]


    if calc == '/':
        if i2 == 999: i2 = i


    if '(' in comp_unit:
        m = re.search(r"\([^\)]+\)", comp_unit)
        power_str = m.group()[1:-1]
        if '.' in power_str: power = float(power_str)
        else: power = int(power_str)
        comp_unit = comp_unit.replace(m.group(), "")
    else:
        power = 1


    X, D_CATE = [], []
    for symbol in COMP_UNIT[comp_unit].keys():
        factor = COMP_UNIT[comp_unit][symbol]["factor"]
        factor **= power

        if calc == '/':
            if comp_unit == "temperature": factor = 1
            else: factor = 1/factor

        symbols = edit_symbol(symbol, calc, power)         # f
        for s in symbols:
            if s == "": continue
            if s in text:
                if not [s, factor] in X: X.append([s, factor])


    return X, calc, i2



def edit_symbol(symbol, calc, power):
    # For example, (cm3)-0.5.
    #     symbol_1="cm3",   symbol_2="/cm3",   symbol_3="cm-3",
    #     symbol_4="cm1.5", symbol_5="/cm1.5", symbol_6="cm-1.5",
    #     symbol_7="cm3/2", symbol_8="/cm3/2", symbol_9="cm-3/2",


    symbol_1 = symbol
    symbol_2, symbol_3, symbol_4, symbol_5, symbol_6, symbol_7, symbol_8, symbol_9 = "", "", "", "", "", "", "", ""

    if not symbol[-1].isnumeric(): symbol += '1'
    power_2 = int(symbol[-1])

    if calc == '/':
        symbol_2 = '/' + symbol
        symbol_3 = symbol[:-1] + str(-power_2)


    if power != 1:
        power *= power_2
        if type(power) is int:
            symbol_4 = symbol[:-1] + str(power)
            if calc == '/':
                symbol_5 = '/' + symbol_4
                symbol_6 = symbol[:-1] + str(-power)
        elif type(power) is float:
            symbol_4, symbol_7 = decimal_and_fraction_notation(symbol[:-1], power)    # f
            if calc == '/':
                symbol_6, symbol_9 = decimal_and_fraction_notation(symbol[:-1], -power)    # f
                symbol_5 = '/' + symbol_4
                symbol_8 = '/' + symbol_7


    symbols = [symbol_1, symbol_2, symbol_3, symbol_4, symbol_5, symbol_6, symbol_7, symbol_8, symbol_9]


    return symbols



def decimal_and_fraction_notation(symbol, power):
    power_str = "{:.1f}".format(power)
    symbol_deci = symbol + power_str
    a = Fraction(power_str)
    power_str_f = str(a.limit_denominator(10))
    symbol_fra = symbol + power_str_f

    return symbol_deci, symbol_fra



def create_notation_pattern(P, calc, i2, start, stop):
    PAT = []
    for X in P:
        Y1 = list(map(lambda a: a[0], list(X)))
        judge = check_division_form(Y1, i2)                                    # f
        # if judge == 0: continue

        Y2 = list(map(lambda a: a[1], list(X)))
        factor = math.prod(Y2)

        if start != -1:
            P2 = itertools.permutations(Y1[start:stop+1])
            for V in P2:
                Z = Y1[:start]
                Z.extend(list(V))
                if stop < len(Y1) - 1: Z.extend(Y1[stop+1:])
                PAT.append([Z, factor, calc, i2, len("".join(Z))])
        else:
            PAT.append([Y1, factor, calc, i2, len("".join(Y1))])


    PAT = sorted(PAT, key = lambda a:(-a[-1]))    # Prefer longer notation.


    return PAT



def check_division_form(SYMBOL, i2):
    judge = 1
    for i, symbol in enumerate(SYMBOL):
        if i >= i2:
            m = re.search(r"(^/|-[1-9]$)", symbol)
            if i == i2:
                if m:
                    if m.groups()[0] is not None: a = 0
                    else: a = 1
                else: a = -1
            else:
                if m:
                    if a != -1:
                        if m.groups()[a] is None:
                            judge = 0
                            break
                    else:
                        judge = 0
                        break
                else:
                    if a != -1:
                        judge = 0
                        break

    return judge



def recognize_unit(OK_TEXT, PAT, d_factor, text):
    value_2, judge = '_', 0
    judge, match, factor = 0, '_', 1
    for x in PAT:
        X, factor, calc, start_div = x[:-1]
        judge, match = check_unit_notation_by_RE(OK_TEXT, X, text, calc, start_div)    # f
        if judge == 1: break

    return judge, match, factor, d_factor



def check_unit_notation_by_RE(OK_TEXT, SYMBOL, text, calc, start_div):
    META_CHAR = ["\.", "\[", "\]", "\-", "\^", "\$", "\*" "\+", "\?", "\{", "\}", "\(", "\)"]
    for i in range(len(SYMBOL)):
        for meta in META_CHAR:
            SYMBOL[i] = SYMBOL[i].replace(meta[1], meta)

    X = list(map(lambda a: '(' + a + ")(.{0,3})", SYMBOL))
    # x = "(.{0,1})" + "".join(X)[:-len("(.{0,3})")] + "(.{0,1})"
    x = "(.{0,1})" + "".join(X)[:-len("(.{0,3})")] + "([a-z]?)" + "(.{0,1})"
    pat = re.compile(r"%s" % x)
    M = pat.findall(text)

    judge, match = check_all_matches(M, OK_TEXT)                               # f


    return judge, match



def check_all_matches(M, OK_TEXT):
    judge, match = 0, '_'
    for m in M:
        judge = 1

        for j, x in enumerate(m[::2]):
            if j == len(m[::2]) - 1: x = m[-1]
            for ok in OK_TEXT:
                if x == "": break
                x = x.replace(ok, "")
            if x != "":
                judge = 0
                break

        if judge == 1:
            match = "".join(m[1:-2])
            break


    return judge, match


