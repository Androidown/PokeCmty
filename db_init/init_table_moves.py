#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import os
from cmntbl.models import *
from db_init import yield_valid_pm
from db_init.tools import ALL_MOVES

BASE = os.path.dirname(__file__)

TYPES_EN = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy"]
html = os.path.join(BASE, 'data/moves.html')
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
        kwargs = {}
        idx = int(record[0])
        kwargs['move_CHS'] = ALL_MVOES[idx]
        kwargs['move_EN'] = ALL_MVOES_EN[idx]
        kwargs['pp'] = int(record[5].replace('*', ''))
        power = record[6].replace('*', '')
        if power.isdigit():
            kwargs['power'] = int(power)

        acc = record[7].replace('*', '').replace('%', '')

        if acc.isdigit():
            kwargs['accuracy'] = int(acc)

        category = ["Physical", "Special", "Status", "???"].index(record[3])
        kwargs['category'] = MoveCategory.objects.get(pk=category)

        mv_type_id = TYPES_EN.index(record[2])
        kwargs['mv_type'] = Types.objects.get(pk=mv_type_id)
        Moves.objects.create(**kwargs)


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
        kwargs['bin_move'] = move_int.to_bytes(128, 'little', signed=False)

        LearnableMove.objects.create(**kwargs)
