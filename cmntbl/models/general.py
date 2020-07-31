from django.db import models
from cmntbl.models.fields import PositiveTinyIntegerField

__all__ = ['Types', 'Ability', 'PokeMon']


class Types(models.Model):
    type_id = PositiveTinyIntegerField(primary_key=True, unique=True, default=0)
    type_CHS = models.CharField(max_length=2)

    def __str__(self):
        return self.type_CHS


class Ability(models.Model):
    ability_CHS = models.CharField(max_length=10)
    ability_EN = models.CharField(max_length=30)
    ability_JP = models.CharField(max_length=16)
    description = models.CharField(max_length=80)


# Create your models here.
class PokeMon(models.Model):
    pkm_id = models.PositiveIntegerField(primary_key=True, unique=True)
    species = models.PositiveSmallIntegerField()
    form = PositiveTinyIntegerField(default=0)
    HP = PositiveTinyIntegerField()
    ATK = PositiveTinyIntegerField()
    DEF = PositiveTinyIntegerField()
    SPA = PositiveTinyIntegerField()
    SPD = PositiveTinyIntegerField()
    SPE = PositiveTinyIntegerField()
    type1 = models.ForeignKey(Types, on_delete=models.DO_NOTHING, related_name="type_str1", default=0, unique=False)
    type2 = models.ForeignKey(Types, on_delete=models.DO_NOTHING, related_name="type_str2", null=True, unique=False)
    ability1 = models.ForeignKey(Ability, on_delete=models.DO_NOTHING, related_name="abl_str1", default=0, unique=False)
    ability2 = models.ForeignKey(Ability, on_delete=models.DO_NOTHING, related_name="abl_str2", default=0, unique=False)
    abilityH = models.ForeignKey(Ability, on_delete=models.DO_NOTHING, related_name="abl_strH", default=0, unique=False)
    name_CHS = models.CharField(max_length=5)

    class Meta:
        unique_together = ("species", "form")

    def __str__(self):
        return self.name_CHS
