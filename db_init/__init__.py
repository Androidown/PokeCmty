#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from cached_property import cached_property

BASE = os.path.dirname(__file__)


def load_personal(game_ver="swsh"):
    db_path = os.path.join(BASE, f"data/personal_{game_ver}")
    if not os.path.isfile(db_path):
        raise FileNotFoundError(db_path)
    db = open(db_path, 'rb').read()
    return db


def to_uint(byte_value, start, bit_len):
    end = start + int(bit_len/8)
    return int.from_bytes(byte_value[start: end], byteorder=sys.byteorder, signed=False)


def get_flag(byte_value, byte_idx, bit_idx):
    bit_idx &= 7
    return ((byte_value[byte_idx] >> bit_idx) & 1) != 0


PERSONAL_SWSH = load_personal()


class PKMPersonal(object):
    def __init__(self, species: int, form=0):
        self.species = species
        self.form = form
        pm_size = 0xB0
        byte_start = species * pm_size
        personal = PERSONAL_SWSH[byte_start: byte_start+pm_size]
        form_cnt = personal[0x20]
        form_stats_index = to_uint(personal, 0x1E, 16)
        if 0 < form < form_cnt and form_cnt > 1:
            byte_start = (form_stats_index + form - 1) * pm_size
            self.personal = PERSONAL_SWSH[byte_start: byte_start+pm_size]
        else:
            self.personal = personal

    @cached_property
    def real_index(self):
        if self.form == 0 or self.forme_count == 1:
            return self.species
        else:
            return self.form_stats_index + self.form - 1

    @cached_property
    def abilities(self):
        return [to_uint(self.personal, 0x18+i, 16) for i in range(0, 6, 2)]

    @cached_property
    def forme_count(self):
        return self.personal[0x20]

    @cached_property
    def forme_sprite(self):
        return to_uint(self.personal, 0x1E, 16)

    @cached_property
    def sprite_forme(self):
        return ((self.personal[0x21] >> 7) & 1) == 1

    @cached_property
    def form_stats_index(self):
        if self.forme_count > 1:
            return to_uint(self.personal, 0x1E, 16)
        return self.species

    @cached_property
    def form_index(self):
        return to_uint(self.personal, 0x5E, 16)

    @cached_property
    def base_species(self):
        return to_uint(self.personal, 0x56, 16)

    @cached_property
    def base_species_form(self):
        return to_uint(self.personal, 0x58, 16)

    @cached_property
    def gender(self):
        return self.personal[0x12]

    @cached_property
    def HP(self):
        # if self.species == 891:
        #     return 60
        # if self.species == 892:
        #     return 100
        return self.personal[0x00]

    @cached_property
    def STAS(self):
        # if self.species == 891:
        #     return [90, 60, 72, 53, 50]
        # if self.species == 892:
        #     return [130, 100, 97, 63, 60]
        return [
            self.personal[0x01],
            self.personal[0x02],
            self.personal[0x03],
            self.personal[0x04],
            self.personal[0x05],
        ]

    @cached_property
    def real_species(self):
        if self.forme_count <= 1 or self.form == 0:
            return self.species
        return self.form_stats_index + self.form - 1

    @cached_property
    def real_base(self):
        return PKMPersonal(self.base_species, self.base_form).real_species

    @cached_property
    def base_form(self):
        base = PKMPersonal(self.base_species)
        if base.forme_count == 1:
            return 0
        if base.forme_count == self.forme_count:
            return self.form
        if base.forme_count > self.forme_count:
            if base.forme_count == 2:
                return 1
            if self.species == 53:  # 猫老大
                return self.form
            if self.species == 863:  # 喵头目
                return 2
        # base.forme_count < self.forme_count
        if self.species == 745:  # 鬃岩狼人
            return self.form // 2
        if self.species in {80, 555}:  # 达摩狒狒
            return min(self.form, 1)

    @cached_property
    def type1(self):
        return self.personal[0x06]

    @cached_property
    def type2(self):
        return self.personal[0x07]

    @cached_property
    def type_tutor(self):
        return [get_flag(self.personal, 0x38, i) for i in range(8)]


def yield_valid_pm():
    for i in range(893):
        pm = PKMPersonal(i)
        if pm.HP == 0:
            continue
        for alter in range(pm.forme_count):
            pm_a = PKMPersonal(i, alter)
            if pm_a.HP == 0:
                continue
            yield pm_a

