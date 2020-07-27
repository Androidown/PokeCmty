from django.shortcuts import render, get_object_or_404
from .models import PokeMon

# def show_pkms(requset, species=1, form=0):
#     return render(requset, 'pkmstat/base_list.html', {'pokemons': PokeMon().get_first_n_pokemons(species)})


def show_stats(request, species=1, form=0):
    pkm = get_object_or_404(PokeMon, species=species, form=form)
    return render(request, 'pkmstat/pkm_detail.html', {'pokemon': pkm})


def display_meta(request):
    return render(request, 'pkmstat/display_meta.html', {'meta': request.META})


def search(request):
    key = request.GET.get('key')
    if not key:
        return render(request, 'pkmstat/search.html')
    if key.isdigit():
        rslt = PokeMon.objects.filter(species=key)
    else:
        rslt = PokeMon.objects.filter(name_CHS__startswith=key)
    return render(request, 'pkmstat/search_rslt.html', {'pkms': rslt, 'key': key})
