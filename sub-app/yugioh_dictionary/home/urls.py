from django.urls import path, include
from . import views

app_name = views.app_name
urlpatterns = [
    path('', views.main_view, name="main"),
    path('decklist/', include('decklist.urls')),
]
