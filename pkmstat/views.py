from django.shortcuts import render, get_object_or_404
from .models import PokeMon

# def show_pkms(requset, species=1, form=0):
#     return render(requset, 'pkmstat/base_list.html', {'pokemons': PokeMon().get_first_n_pokemons(species)})


def show_stats(requset, species=1, form=0):
    pkm = get_object_or_404(PokeMon, species=species, form=form)
    return render(requset, 'pkmstat/pkm_detail.html', {'pokemon': pkm})
