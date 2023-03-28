def file_list(indir, EXT, SW=None):
    import os

    INFNAME0 = os.listdir(indir)
    INFNAME = []
    for x in INFNAME0:
        for ext in EXT:
            if x.endswith(ext):
                check_sw = 0
                if SW is not None:
                    for sw in SW:
                        if sw in x:
                            check_sw = 1
                            break
                if check_sw == 0: INFNAME.append(x)

    return INFNAME



def input_data(infname, tab, blanc_line):
    with open(infname, "r", encoding = "utf-8") as inf:
        INPUT = []
        for x in inf:
            x = x[:-1]    # rstrip()
            if blanc_line == 1 and x == "": continue
            if tab == 1: x = x.split("\t")
            INPUT.append(x)

    return INPUT



def edit_for_output(HEADER, OUTPUT):
    OUTPUT_2 = []
    for x in HEADER: OUTPUT_2.append("\t".join(x))
    for i, x in enumerate(OUTPUT): OUTPUT_2.append("\t".join(x))

    return OUTPUT_2



def output(outfname, OUTPUT, sep=None):
    with open(outfname, "w", encoding = "utf-8") as f:
        for x in OUTPUT:
            if sep is None: print(x, file=f)
            else: print(*x, sep=sep, file=f)



def make_tmpdir(basedir=None, remove=False, dirname="tmpdir"):
    import os, shutil

    if basedir is None: basedir = os.getcwd()
    tmpdir = basedir + "/" + dirname
    if remove is True:
        if dirname in os.listdir(basedir): shutil.rmtree(tmpdir)
    os.makedirs(tmpdir, exist_ok = True)

    return tmpdir



def delete_directory(deldir):
    import shutil

    shutil.rmtree(deldir)



def iter_end(DATA, start, end_word, stop_word=None, CHECK_J=None):
    j2 = -1
    for j in range(start, len(DATA)):
        if CHECK_J != None:
            if j in CHECK_J: continue
        if end_word in DATA[j]:
            j2 = j
            break
        if stop_word != None:
            if stop_word in DATA[j]: break

    return j2



def extract_BIES_tagged_entity(TOK, TAG, del_tok_whitespace):
    ENTITY, TOKID = [], []
    for i, tok in enumerate(TOK):
        tag = TAG[i]
        if tag[0] in ["S", "B"]:
            j2 = -1
            if tag[0] == "S": j2 = i
            elif tag[0] == "B":
                for j in range(i + 1, len(TOK)):
                    if TAG[j][0] in ["S", "O"]: break
                    elif TAG[j][0] == "E":
                        j2 = j
                        break
            if j2 != -1:
                entity = " ".join(TOK[i : j2 + 1])
                if del_tok_whitespace == 1:
                    entity = entity.replace(" ( ", "(").replace(" ) ", ")").replace(" )", ")").replace(" { ", "{").replace(" } ", "}").replace(" }", "}").replace(" [ ", "[").replace(" [", "[").replace(" ] ", "]").replace(" ]", "]").replace(" / ", "/").replace(" /", "/").replace("/ ", "/").replace(" , ", ",").replace(", ", ",").replace(" ,", ",").replace(" - ", "-").replace("- ", "-").replace(" -", "-")
                ENTITY.append(entity)
                TOKID.append([i + 1, j2 + 1])

    LONG_ABB = []
    for i in range(len(TOKID) - 1):
        if TOKID[i + 1][0] - TOKID[i][1] == 2:
            a = TOKID[i][1]    # TOKID is not started from zero, but one.
            if TOK[a] in ["(", "[", ","]:
                long, abb = ENTITY[i], ENTITY[i + 1]
                # if len(re.findall(r"[A-Z]", abb)) / len(abb) >= 0.5:
                X = [long, abb]
                if not X in LONG_ABB: LONG_ABB.append(X)


    for x in TOKID: x[0], x[1] = str(x[0]), str(x[1])


    return ENTITY, TOKID, LONG_ABB



def get_datetime(mode):
    import datetime

    dt_now = datetime.datetime.now()
    if mode == "dt":
        d = dt_now.isoformat().split('.')[0]
        d = d[2:].replace("-", "").replace(":", "").replace("T", "-")
        d = d[:-2]
    elif mode == "d":
        d = dt_now.isoformat().split('T')[0]
        d = d[2:].replace("-", "")


    return d



def iou(bbox1, bbox2):
    s1 =(bbox1[2]- bbox1[0]) * (bbox1[3]- bbox1[1])
    s2 =(bbox2[2]- bbox2[0]) * (bbox2[3]- bbox2[1])

    left_line = max(bbox1[1], bbox2[1])
    right_line = min(bbox1[3], bbox2[3])
    top_line = max(bbox1[0], bbox2[0])
    bottom_line = min(bbox1[2], bbox2[2])

    w = max(0, right_line - left_line)
    h = max(0, bottom_line - top_line)
    intersect = w * h
    union = s1 + s2 - intersect


    return intersect, union, s1, s2


