from django.shortcuts import render, get_object_or_404
from cmntbl.models import PokeMon, LearnableMove, Moves
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView

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


class PokMonList(ListView):
    model = PokeMon
    template_name = 'pkmstat/poke_dex.html'

    def get_queryset(self):
        return self.model.objects.\
            select_related('ability1', 'ability2', 'abilityH', 'type1', 'type2').\
            all().order_by('pkm_id')


class PokeMonSearchList(PokMonList):
    template_name = 'pkmstat/search_rslt.html'

    def get(self, request, *args, **kwargs):
        key = request.GET.get('key')
        if not key:
            return render(request, 'pkmstat/search.html')
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        key = self.request.GET.get('key')
        if key.isdigit():
            queryset = self.model.objects.\
                select_related('ability1', 'ability2', 'abilityH', 'type1', 'type2').\
                filter(species=key).order_by('pkm_id')
        else:
            queryset = self.model.objects.\
                select_related('ability1', 'ability2', 'abilityH', 'type1', 'type2').\
                filter(name_CHS__contains=key).order_by('pkm_id')
        return queryset

    def get_context_data(self):
        return super().get_context_data(key=self.request.GET.get('key'))


def nearby_pkm(request, species, loc):
    if loc == 'next':
        pkm = PokeMon.objects.values_list('species', flat=True).filter(species__gt=species).order_by('pkm_id')[:1]
    elif loc == 'prev':
        pkm = PokeMon.objects.values_list('species', flat=True).filter(species__lt=species, pkm_id__lt=species).order_by('pkm_id').reverse()[:1]
    
    if not pkm:
        raise Http404(f"Pokemon #{species} has no {loc} Pokemon.")

    return HttpResponseRedirect(f"/stat/{pkm[0]}")






