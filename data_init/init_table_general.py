#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from bs4 import BeautifulSoup
from cmntbl.models import *
from data_init import yield_valid_pm, BASE


def init_table_abilities():
    html = os.path.join(BASE, 'data/abilities.html')
    with open(html, 'rt', encoding='utf8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    tables = [
        [td.get_text(strip=True) for td in tr.find_all('td')]
        for table in soup.find_all('table') for tr in table.find_all('tr')
    ]
    for idx, row in enumerate(tables, 1):
        kwargs = {
            'ability_CHS': row[1],
            'ability_JP': row[2],
            'ability_EN': row[3],
            'description': row[4],
        }
        Ability.objects.create(**kwargs)


def init_table_types():
    types_CHS = ["一般", "格斗", "飞行", "毒", "地面", "岩石", "虫", "幽灵", "钢", "火", "水", "草", "电", "超能", "冰", "龙", "恶", "妖精",]
    types_EN = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "Fire", "Water",
                "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy"]
    for tid, (text_CHS, text_EN) in enumerate(zip(types_CHS, types_EN)):
        Types.objects.create(type_id=tid, type_CHS=text_CHS, type_EN=text_EN)


def init_table_pokemon():
    with open(os.path.join(BASE, f"data/species_9"), "rt", encoding="utf8") as db:
        SPECIES = db.read().splitlines()
    for pkm in yield_valid_pm():
        kwargs = {
            'pkm_id': pkm.real_species,
            'species': pkm.species,
            'form': pkm.form,
            'HP': pkm.HP,
            'ATK': pkm.STAS[0],
            'DEF': pkm.STAS[1],
            'SPA': pkm.STAS[3],
            'SPD': pkm.STAS[4],
            'SPE': pkm.STAS[2],
            'type1': Types.objects.get(type_id=pkm.type1),
            'ability1': Ability.objects.get(pk=pkm.abilities[0]),
            'ability2': Ability.objects.get(pk=pkm.abilities[1]),
            'abilityH': Ability.objects.get(pk=pkm.abilities[2]),
            'name_CHS': SPECIES[pkm.species]
        }
        if not pkm.type2 == pkm.type1:
            kwargs['type2'] = Types.objects.get(type_id=pkm.type2)
        PokeMon.objects.create(**kwargs)
