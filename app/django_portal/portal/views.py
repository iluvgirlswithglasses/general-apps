from django.shortcuts import render
import os

# Create your views here.
def get(request):
    STATIC_URL = os.getcwd() + "/portal/static/f/"
    lst = {}
    for folder in os.listdir(STATIC_URL):
        lst[folder] = os.listdir(STATIC_URL + folder)
    #
    return render(request, "homepage.html", {
        "lst": lst,
    })
