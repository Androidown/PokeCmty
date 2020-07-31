#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from db_init import BASE, PKMPersonal
import os

EvoSpecies = {
    1: [2], 2: [3], 4: [5], 5: [6], 7: [8], 8: [9], 10: [11], 11: [12], 25: [26], 27: [28], 906: [907], 35: [36],
    37: [38], 908: [909], 39: [40], 43: [44], 44: [45, 182], 50: [51], 910: [911], 52: [53], 912: [914], 913: [863],
    54: [55], 58: [59], 60: [61], 61: [62, 186], 63: [64], 64: [65], 66: [67], 67: [68], 72: [73], 77: [78], 918: [919],
    79: [80, 199], 920: [922], 81: [82], 82: [462], 923: [865], 90: [91], 92: [93], 93: [94], 95: [208], 98: [99],
    102: [103], 104: [105], 108: [463], 109: [928], 111: [112], 112: [464], 113: [242], 114: [465], 116: [117],
    117: [230], 118: [119], 120: [121], 929: [866], 123: [212], 129: [130],
    133: [470, 471, 135, 134, 136, 700, 196, 197], 137: [233], 163: [164], 170: [171], 172: [25], 173: [35], 174: [39],
    175: [176], 176: [468], 177: [178], 183: [184], 194: [195], 215: [461], 220: [221], 221: [473], 957: [864],
    223: [224], 233: [474], 236: [107, 106, 237], 246: [247], 247: [248], 263: [264], 958: [959], 959: [862],
    270: [271], 271: [272], 273: [274], 274: [275], 278: [279], 280: [281], 281: [282, 475], 290: [291], 293: [294],
    294: [295], 298: [183], 309: [310], 315: [407], 318: [319], 320: [321], 328: [329], 329: [330], 339: [340],
    341: [342], 343: [344], 349: [350, 350], 355: [356], 356: [477], 360: [202], 361: [362, 478], 403: [404],
    404: [405], 406: [315], 415: [416], 420: [421], 422: [423], 974: [975], 425: [426], 427: [428], 434: [435],
    436: [437], 438: [185], 439: [929], 440: [113], 446: [143], 447: [448], 449: [450], 451: [452], 453: [454],
    458: [226], 459: [460], 506: [507], 507: [508], 509: [510], 517: [518], 519: [520], 520: [521], 524: [525],
    525: [526], 527: [528], 529: [530], 532: [533], 533: [534], 535: [536], 536: [537], 543: [544], 544: [545],
    546: [547], 548: [549], 551: [552], 552: [553], 554: [555], 1001: [1003], 557: [558], 559: [560], 562: [563],
    1005: [867], 568: [569], 570: [571], 572: [573], 574: [575], 575: [576], 577: [578], 578: [579], 582: [583],
    583: [584], 588: [589], 590: [591], 592: [593], 595: [596], 597: [598], 599: [600], 600: [601], 605: [606],
    607: [608], 608: [609], 610: [611], 611: [612], 613: [614], 616: [617], 619: [620], 622: [623], 624: [625],
    627: [628], 629: [630], 633: [634], 634: [635], 636: [637], 659: [660], 661: [662], 662: [663], 674: [675],
    677: [678, 1105], 679: [680], 680: [681], 682: [683], 684: [685], 686: [687], 688: [689], 690: [691], 692: [693],
    694: [695], 704: [705], 705: [706], 708: [709], 710: [711], 1107: [1110], 1108: [1111], 1109: [1112], 712: [713],
    714: [715], 722: [723], 723: [724], 725: [726], 726: [727], 728: [729], 729: [730], 736: [737], 737: [738],
    742: [743], 744: [745, 1123], 1122: [1124], 747: [748], 749: [750], 751: [752], 753: [754], 755: [756], 757: [758],
    759: [760], 761: [762], 762: [763], 767: [768], 769: [770], 772: [773], 782: [783], 783: [784], 789: [790],
    790: [791, 792], 810: [811], 811: [812], 813: [814], 814: [815], 816: [817], 817: [818], 819: [820], 821: [822],
    822: [823], 824: [825], 825: [826], 827: [828], 829: [830], 831: [832], 833: [834], 835: [836], 837: [838],
    838: [839], 840: [841, 842], 843: [844], 846: [847], 848: [849, 1162], 850: [851], 852: [853], 854: [855],
    1163: [1164], 856: [857], 857: [858], 859: [860], 860: [861],
    868: [869, 1165, 1166, 1167, 1168, 1169, 1170, 1171, 1172], 872: [873], 878: [879], 885: [886], 886: [887],
    891: [892, 1179]
}


def yield_all_evos(form_stat_idx):
    evos = EvoSpecies.get(form_stat_idx, None)
    if evos is not None:
        for idx in evos:
            yield idx
            yield from yield_all_evos(idx)


PF = os.path.join(BASE, "data/Pokemon - Sword 1.2.0.txt")

with open(os.path.join(BASE, "data/moves_en"), "rt", encoding="utf8") as db:
    MOVE_TXT = db.read().splitlines()


TYPE_TUTOR = [520, 519, 518, 338, 307, 308, 434, 796]


def load_lvlmoves():
    rtn = {}
    pm_added = False
    pm_ready = False
    egg_move_found = False
    cur_pm = 0
    with open(PF, 'rt', encoding='utf-8') as f:
        for line in f:
            line = line.replace("\n", '')
            if pm_ready and not pm_added:
                cur_pm = int(line.split('-')[0].strip())
                rtn[cur_pm] = []
                pm_added = True

            if line == "======":
                if not pm_added:
                    pm_ready = True
                else:
                    pm_added = False
                    pm_ready = False

            if egg_move_found:
                if line.startswith('-'):
                    lvl, move = line.split(']')
                    lvl = int(lvl.split('[')[-1])
                    move = move.strip()
                    rtn[cur_pm].append(MOVE_TXT.index(move))
                else:
                    egg_move_found = False

            if line == "Level Up Moves:":
                egg_move_found = True

    return rtn


def load_eggmoves():
    rtn = {}
    pm_added = False
    pm_ready = False
    egg_move_found = False
    cur_pm = 0
    with open(PF, 'rt', encoding='utf-8') as f:
        for line in f:
            line = line.replace("\n", '')
            if pm_ready and not pm_added:
                cur_pm = int(line.split('-')[0].strip())
                rtn[cur_pm] = []
                pm_added = True

            if line == "======":
                if not pm_added:
                    pm_ready = True
                else:
                    pm_added = False
                    pm_ready = False

            if egg_move_found:
                if line.startswith('-'):
                    rtn[cur_pm].append(MOVE_TXT.index(line[2:]))
                else:
                    egg_move_found = False

            if line == "Egg Moves:":
                egg_move_found = True

    return rtn


def load_TMTR(tech):
    rtn = {}
    pm_added = False
    pm_ready = False
    egg_move_found = False
    cur_pm = 0
    with open(PF, 'rt', encoding='utf-8') as f:
        for line in f:
            line = line.replace("\n", '')
            if pm_ready and not pm_added:
                cur_pm = int(line.split('-')[0].strip())
                rtn[cur_pm] = []
                pm_added = True

            if line == "======":
                if not pm_added:
                    pm_ready = True
                else:
                    pm_added = False
                    pm_ready = False

            if egg_move_found:
                if egg_move_found:
                    if line.startswith('-'):
                        _, move = line.split(']')
                        move = move.strip()
                        rtn[cur_pm].append(MOVE_TXT.index(move))
                    else:
                        egg_move_found = False
                else:
                    egg_move_found = False

            if line == tech + "s:":
                egg_move_found = True

    return rtn


def load_tutors():
    rtn = {}
    pm_added = False
    pm_ready = False
    egg_move_found = False
    cur_pm = 0
    with open(PF, 'rt', encoding='utf-8') as f:
        for line in f:
            line = line.replace("\n", '')
            if pm_ready and not pm_added:
                cur_pm = int(line.split('-')[0].strip())
                rtn[cur_pm] = []
                pm_added = True

            if line == "======":
                if not pm_added:
                    pm_ready = True
                else:
                    pm_added = False
                    pm_ready = False

            if egg_move_found:
                if line.startswith('-'):
                    rtn[cur_pm].append(MOVE_TXT.index(line[2:]))
                else:
                    egg_move_found = False

            if line == "Armor Tutors:":
                egg_move_found = True

    return rtn


egg_moves = load_eggmoves()
lvl_moves = load_lvlmoves()
trs = load_TMTR("TR")
tms = load_TMTR("TM")
tutors = load_tutors()

assert len(egg_moves) == len(lvl_moves) == len(trs) == len(tms) == len(tutors)

all_moves = {}

for k in egg_moves:
    tu_flag = PKMPersonal(k).type_tutor
    type_tutors = [TYPE_TUTOR[i] for i in range(8) if tu_flag[i]]
    all_moves[k] = set(egg_moves[k] + lvl_moves[k] + trs[k] + tms[k] + tutors[k] + type_tutors)

VOLT_TACKLE = 344
all_moves[172].add(VOLT_TACKLE)

for k in all_moves:
    for evo in yield_all_evos(k):
        all_moves[evo] = all_moves[evo].union(all_moves[k])


ALL_MOVES = all_moves
