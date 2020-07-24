from django.db import models


class PositiveTinyIntegerField(models.PositiveIntegerField):
    description = "Unsigned Tiny Integer."

    def db_type(self, connection):
        return "TINYINT UNSIGNED"

    def rel_db_type(self, connection):
        return "TINYINT UNSIGNED"


# Create your models here.
class PokeMon(models.Model):
    species = models.PositiveSmallIntegerField()
    form = PositiveTinyIntegerField(default=0)
    HP = PositiveTinyIntegerField()
    ATK = PositiveTinyIntegerField()
    DEF = PositiveTinyIntegerField()
    SPA = PositiveTinyIntegerField()
    SPD = PositiveTinyIntegerField()
    SPE = PositiveTinyIntegerField()
    type1 = PositiveTinyIntegerField()
    type2 = PositiveTinyIntegerField(null=True)
    ability1 = models.PositiveSmallIntegerField(default=0)
    ability2 = models.PositiveSmallIntegerField(default=0)
    abilityH = models.PositiveSmallIntegerField(default=0)
    name_CHS = models.CharField(max_length=5)

    class Meta:
        unique_together = ("species", "form")
    #
    #
    # def get_basic_stats(self, spcs, forme):
    #     try:
    #         PokeMon.objects.get(species=spcs, form=forme)
    #
    #
    # def get_first_n_pokemons(self, n):
    #     return PokeMon.objects.filter(pk__lte=n)
