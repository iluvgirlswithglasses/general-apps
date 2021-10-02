from django.db import models
from home.engine import typ, get_deck_of

# Create your models here.
class Card(models.Model):
    def __str__(self):
        return "[{}][{}] - {}".format(self.id, typ[self.typ], self.name)

    def to_json(self):
        res = {}
        for i in ['id', 'typ', 'name']:
            res[i] = getattr(self, i)
        # effect
        res['eff'] = ''
        for i in self.eff:
            if i == '\n':
                res['eff'] += '<br/>'
            else:
                res['eff'] += i
        return res

    typ = models.IntegerField(default=0, null=False, blank=False)
    name = models.CharField(default="", max_length=128, null=False, blank=False)
    eff = models.TextField(default="", null=True, blank=True)

class Deck(models.Model):
    def __str__(self):
        return self.name

    def get_cards(self):
        cards = [[], []]
        for i in self.cards_pattern.split(' '):
            card = Card.objects.get(id=i)
            cards[get_deck_of(card.typ)].append(card.to_json())
        return cards

    name = models.CharField(default="", max_length=64, null=False, blank=False)
    cards_pattern = models.CharField(default="", max_length=512)
