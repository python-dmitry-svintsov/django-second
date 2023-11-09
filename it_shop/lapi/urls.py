from django.urls import path
from .views import Lapi_Main, Lapi_Game, Get_Data

urlpatterns = [
    path('', Lapi_Main.as_view(), name='lapi-home'),
    path('game/<slug:slug>/', Lapi_Game.as_view(), name='lapi-game'),
    path('get_data/<slug:slug>/', Get_Data.as_view())
]