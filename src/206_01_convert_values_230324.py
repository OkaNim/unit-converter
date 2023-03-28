# import
import os, sys, json, re
import src_001_basic_221017 as src_001
import src_206_unit_convertor_230324 as src_206




# main
def main():
    args = sys.argv
    if len(args) > 1:
        indir = args[1]
        outdir = indir
    else:
        indir = "../out/01_input-data"
        outdir = "../out/02_result"


    props = [
                "electric-conductivity",
                "gas-permeability-coeff",
                "gas-permeability-coeff_non_barrer",
                "glass-transition-temp",
                "half-time-crystal",
                "solubility-parameter",
                "specific-heat-capacity-Cp",
            ]


    infname = props[1] + "_ca.json"
    print("\n\n\t", infname, "\n")
    with open(indir + '/' + infname) as f: data = json.load(f)


    ccu_file = infname.split('_')[0] + "_CCU.txt"    # ""    # "unitless_CCU.txt"
    texts = []
    for i, xx in enumerate(data["data"]):
        x = xx["data_point"]

        prop_spec, value, rel_tcd, tcap, tfoot = x["prop_spec"], x["value"], x["related_tcd"], x["caption"], x["footnote"]
        text = [prop_spec, rel_tcd, tfoot, tcap]
        results = src_206.main(ccu_file, value, text)                          # i
        xx["unit_conversion"] = results

        if "unit_conversion_ca" in xx:
            cas = xx["unit_conversion_ca"]
            tf_power_10, tf_value_cl, tf_unit, tf_value_cv = evaluate_results(results, cas)    # f
            xx["evaluation"] = {"tf_power_10":tf_power_10, "tf_value_cl":tf_value_cl, "tf_unit":tf_unit, "tf_value_cv":tf_value_cv}


    data = calculate_accuracy(data)                                            # f


    outfname = infname.replace("_ca.json", "_convert.json")
    with open(outdir + '/' + outfname, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



    # Print screen
    print("\n\nfinish\n\n")




# f
def evaluate_results(preds, cas):
    power_10, power_10_ca = preds["power_10"], cas["power_10"]
    value_cl, value_cl_ca = preds["value_cl"], cas["value_cl"]
    unit, unit_ca = preds["unit"], cas["unit"]
    value_cv, value_cv_ca = preds["value_cv"], cas["value_cv"]

    tf_power_10 = 0
    if power_10_ca == power_10: tf_power_10 = 1
    tf_value_cl = evaluate_value(value_cl, value_cl_ca)                        # f
    tf_unit = evaluate_unit(unit, unit_ca)                                     # f
    tf_value_cv = evaluate_value(value_cv, value_cv_ca)                        # f


    return tf_power_10, tf_value_cl, tf_unit, tf_value_cv



def evaluate_value(pred, ca):
    tf = 0
    if is_float(pred):                                                         # f
        pred, ca = float(pred), float(ca)
        if ca == 0:
            if abs(pred - ca) < 1e-4: tf = 1
        else:
            if abs(pred/ca - 1) < 1e-4: tf = 1

    return tf



def is_float(text):
    try:
        float(text)
    except:
        return False
    return True



def evaluate_unit(pred, ca):
    tf = 0
    ss = set(pred) ^ set(ca)

    if ss == set(): tf = 1
    else:
        check_j = [j for j in range(len(ss))]
        for j, s in enumerate(ss):
            if re.fullmatch(r"[\(\)\[\]\-]|[0-9]", s): check_j.remove(j)
            if check_j == []: tf = 1


    return tf



def calculate_accuracy(data):
    power_10, value_cl, unit, value_cv = 0, 0, 0, 0
    for xx in data["data"]:
        x = xx["evaluation"]

        power_10 += x["tf_power_10"]
        value_cl += x["tf_value_cl"]
        unit += x["tf_unit"]
        value_cv += x["tf_value_cv"]

    accu_power_10 = "{:.4f}".format(power_10 / len(data["data"]))
    accu_value_cl = "{:.4f}".format(value_cl / len(data["data"]))
    accu_unit = "{:.4f}".format(unit / len(data["data"]))
    accu_value_cv = "{:.4f}".format(value_cv / len(data["data"]))


    xx = {"accu_power_10":accu_power_10, "accu_value_cl":accu_value_cl, "accu_unit":accu_unit, "accu_value_cv":accu_value_cv}


    terms = [power_10, value_cl, unit, value_cv]
    cnt = -1
    for k, v in xx.items():
        cnt += 1
        print("\n\t {}:\t {}\t\t(true={}, false={})".format(k, v, terms[cnt], len(data["data"])-terms[cnt]))
    print("")


    data["data_info"] = dict(**data["data_info"], **xx)


    return data




# main_run
main()

