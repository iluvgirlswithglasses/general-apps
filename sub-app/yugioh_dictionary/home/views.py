from django.shortcuts import render
from .models import Deck

app_name = 'home'
# Create your views here.
def main_view(request):
    return render(request, '{}/base.html'.format(app_name), {
        'decks': Deck.objects.all()
    })
