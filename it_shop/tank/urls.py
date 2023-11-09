from django.urls import path
from .views import Tank_Main, Tank_Game

urlpatterns = [
    path('', Tank_Main.as_view(), name='main'),
    path('game/level=<slug:slug>/', Tank_Game.as_view(), name='game')
]