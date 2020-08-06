#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import os
from cmntbl.models import *
from data_init import yield_valid_pm
from data_init.tools import ALL_MOVES

BASE = os.path.dirname(__file__)

# TYPES_EN = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy"]
TYPES_CHS = ["一般", "格斗", "飞行", "毒", "地面", "岩石", "虫", "幽灵", "钢", "火", "水", "草", "电", "超能力", "冰", "龙", "恶", "妖精", ]

html = os.path.join(BASE, 'data/moves_with_description.html')
with open(html, 'rt', encoding='utf8') as f:
    soup = BeautifulSoup(f, 'html.parser')

table = soup.find('table')
tables = [
    [td.get_text(strip=True) for td in tr.find_all('td')]
    for tr in table.find_all('tr')
]

with open(f"{BASE}/data/moves_zh", "rt", encoding="utf8") as db:
    ALL_MVOES = db.read().splitlines()

with open(f"{BASE}/data/moves_en", "rt", encoding="utf8") as db:
    ALL_MVOES_EN = db.read().splitlines()


def init_table_moves():
    for record in tables:
        if record[0] == '???':
            continue
        kwargs = {}
        idx = int(record[0])
        kwargs['move_CHS'] = ALL_MVOES[idx]
        kwargs['move_EN'] = ALL_MVOES_EN[idx]

        power = record[6]
        if power.isdigit():
            kwargs['power'] = int(power)
        else:
            kwargs['power'] = None

        acc = record[7]
        if acc.isdigit():
            kwargs['accuracy'] = int(acc)
        else:
            kwargs['accuracy'] = None

        pp = record[8]
        if pp.isdigit():
            kwargs['pp'] = int(pp)
        else:
            kwargs['pp'] = None

        category = ["物理", "特殊", "变化", "极巨"].index(record[5])
        kwargs['category'] = MoveCategory.objects.get(pk=category)

        mv_type_id = TYPES_CHS.index(record[4])
        kwargs['mv_type'] = Types.objects.get(pk=mv_type_id)
        kwargs['description'] = record[-1]
        Moves.objects.create(**kwargs)
        # mv = Moves.objects.get(id=idx)
        # for k, v in kwargs.items():
        #     setattr(mv, k, v)
        # mv.save()


def init_table_move_category():
    all_mcs = ["物理", "特殊", "变化", "??"]
    for id_, text in enumerate(all_mcs):
        MoveCategory.objects.create(cid=id_, category_CHS=text)


def init_table_learnablemoves():
    for pkm in yield_valid_pm():
        kwargs = {
            'pkm_id': pkm.real_species,
            'species': pkm.species,
            'form': pkm.form,
        }
        move_int = 0
        for mv in ALL_MOVES[pkm.real_species]:
            move_int += 1 << (mv - 1)
        kwargs['bin_moves'] = move_int.to_bytes(128, 'little', signed=False)

        LearnableMove.objects.create(**kwargs)
