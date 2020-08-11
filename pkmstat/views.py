from django.shortcuts import render, get_object_or_404
from cmntbl.models import PokeMon, LearnableMove, Moves
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

# def show_pkms(requset, species=1, form=0):
#     return render(requset, 'pkmstat/base_list.html', {'pokemons': PokeMon().get_first_n_pokemons(species)})


def show_stats(request, species=1, form=0):
    try:
        pkm = PokeMon.objects.select_related('ability1', 'ability2', 'abilityH').get(species=species, form=form)
        move_raw = LearnableMove.objects.values('bin_moves').get(pk=pkm.pkm_id)
        move_pool = Moves.objects.select_related('mv_type').filter(pk__in=LearnableMove.parse_moves(move_raw['bin_moves']))
    except ObjectDoesNotExist:
        raise Http404(f"Pokemon #{species}-{form} not found.")
    return render(request, 'pkmstat/pkm_detail.html', {'pokemon': pkm, 'move_pool': move_pool})


def display_meta(request):
    return render(request, 'pkmstat/display_meta.html', {'meta': request.META})


def search(request):
    key = request.GET.get('key')
    if not key:
        return render(request, 'pkmstat/search.html')
    if key.isdigit():
        rslt = PokeMon.objects.filter(species=key)
    else:
        rslt = PokeMon.objects.filter(name_CHS__contains=key)
    return render(request, 'pkmstat/search_rslt.html', {'pkms': rslt, 'key': key})


def nearby_pkm(request, species, loc):
    if loc == 'next':
        pkm = PokeMon.objects.values_list('species', flat=True).filter(species__gt=species).order_by('pkm_id')[:1]
    elif loc == 'prev':
        pkm = PokeMon.objects.values_list('species', flat=True).filter(species__lt=species, pkm_id__lt=species).order_by('pkm_id').reverse()[:1]
    
    if not pkm:
        raise Http404(f"Pokemon #{species} has no {loc} Pokemon.")

    return HttpResponseRedirect(f"/stat/{pkm[0]}")






