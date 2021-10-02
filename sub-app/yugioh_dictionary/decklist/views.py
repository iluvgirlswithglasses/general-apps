from django.shortcuts import render
from django.http import JsonResponse
from home.models import *

app_name = 'decklist'
# Create your views here.
def main_view(request, deck_id):
    return render(
        request, '{}/base.html'.format(app_name), {
            'deck': Deck.objects.get(id=deck_id),
        }
    )

def get_cards(request):
    deck = Deck.objects.get(id=request.GET.get('deck_id'))
    cards = deck.get_cards()
    return JsonResponse({
        'main': cards[0], 'extra': cards[1]
    }, safe=False)
