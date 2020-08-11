#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.db import models
from cmntbl.models.fields import PositiveTinyIntegerField
from .general import Types


__all__ = ['MoveCategory', 'Moves', 'LearnableMove']


class MoveCategory(models.Model):
    cid = PositiveTinyIntegerField(primary_key=True, unique=True, default=0)
    category_CHS = models.CharField(max_length=2)


class Moves(models.Model):
    move_CHS = models.CharField(max_length=8)
    move_EN = models.CharField(max_length=30)
    pp = PositiveTinyIntegerField(null=True)
    power = models.PositiveSmallIntegerField(null=True)
    accuracy = models.PositiveSmallIntegerField(null=True, validators=())
    category = models.ForeignKey(MoveCategory, on_delete=models.DO_NOTHING, null=True, to_field='cid')
    mv_type = models.ForeignKey(Types, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=80)


class LearnableMove(models.Model):
    pkm_id = models.PositiveIntegerField(primary_key=True, unique=True)
    species = models.PositiveIntegerField()
    form = PositiveTinyIntegerField(default=0)
    bin_moves = models.BinaryField(max_length=128)

    class Meta:
        unique_together = ("species", "form")

    @staticmethod
    def parse_moves(binary_moves):
        moves_int = int.from_bytes(binary_moves, 'little', signed=False)
        move_list = []
        idx = 1
        while moves_int:
            if moves_int & 1 == 1:
                move_list.append(idx)
            idx += 1
            moves_int = moves_int >> 1
        return move_list

    @property
    def moves(self):
        return self.parse_moves(self.bin_moves)