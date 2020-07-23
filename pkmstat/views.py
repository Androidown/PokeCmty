from django.shortcuts import render
from django.http import HttpResponse


def show_stats(requset, species=1, form=0):
    return HttpResponse(f"Species is {species}, form is {form}")