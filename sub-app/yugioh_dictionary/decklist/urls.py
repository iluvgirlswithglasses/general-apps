from django.urls import path
from . import views

app_name = views.app_name
urlpatterns = [
    path('<int:deck_id>/', views.main_view, name='base'),
    path('cards/', views.get_cards, name='get_cards'),
]
