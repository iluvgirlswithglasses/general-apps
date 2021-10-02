from django.contrib import admin
from .models import *

# Register your models here.
for i in [Card, Deck]:
    admin.site.register(i)
