from django.db import models
from functools import wraps

# Create your models here.


def set_limit(limit):
    @wraps(set_limit)
    def func(x):
        return x <= limit

    return func


class PositiveTinyIntegerField(models.PositiveIntegerField):
    description = "Unsigned Tiny Integer."

    def db_type(self, connection):
        return "TINYINT UNSIGNED"

    def rel_db_type(self, connection):
        return "TINYINT UNSIGNED"


class Item(models.Model):
    item_CHS = models.CharField(max_length=10)
    description = models.TextField()


class PKMBattleStat(models.Model):
    species = models.PositiveIntegerField()
    form = PositiveTinyIntegerField(default=0)
    ability = models.PositiveIntegerField()
    held_item = models.PositiveIntegerField()

    iv_HP = PositiveTinyIntegerField(default=31, validators=(set_limit(31),))
    iv_ATK = PositiveTinyIntegerField(default=31, validators=(set_limit(31),))
    iv_DEF = PositiveTinyIntegerField(default=31, validators=(set_limit(31),))
    iv_SPA = PositiveTinyIntegerField(default=31, validators=(set_limit(31),))
    iv_SPD = PositiveTinyIntegerField(default=31, validators=(set_limit(31),))
    iv_SPE = PositiveTinyIntegerField(default=31, validators=(set_limit(31),))

    ev_HP = models.PositiveSmallIntegerField(default=0, validators=(set_limit(252),))
    ev_ATK = models.PositiveSmallIntegerField(default=0, validators=(set_limit(252),))
    ev_DEF = models.PositiveSmallIntegerField(default=0, validators=(set_limit(252),))
    ev_SPA = models.PositiveSmallIntegerField(default=0, validators=(set_limit(252),))
    ev_SPD = models.PositiveSmallIntegerField(default=0, validators=(set_limit(252),))
    ev_SPE = models.PositiveSmallIntegerField(default=0, validators=(set_limit(252),))

    move1 = models.PositiveIntegerField()
    move2 = models.PositiveIntegerField()
    move3 = models.PositiveIntegerField()
    move4 = models.PositiveIntegerField()


class Team(models.Model):
    title = models.CharField(max_length=20)
    pkm1 = models.PositiveIntegerField(null=True)
    pkm2 = models.PositiveIntegerField(null=True)
    pkm3 = models.PositiveIntegerField(null=True)
    pkm4 = models.PositiveIntegerField(null=True)
    pkm5 = models.PositiveIntegerField(null=True)
    pkm6 = models.PositiveIntegerField(null=True)


# class MoveManager(models.Manager):
#     def get_learnable_moves(self, species, form):
#         bin_moves = self.get(species=species, form=form).bin_moves
