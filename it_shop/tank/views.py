from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Levels
import sys


def printing(data):
    print(data, file=sys.stdout)


class Tank_Main(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        data = {'data': Levels.objects.order_by('level')}
        return render(request, 'tank/main.html', context=data)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        title = request.POST.get('level')
        slug = Levels.objects.get(title=title)
        return HttpResponseRedirect(reverse_lazy('tank:game', kwargs={'slug': slug}))


class Tank_Game(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response = render(request, 'tank/game.html')
        slug = kwargs['slug']
        obj = Levels.objects.get(slug=slug)
        data = {}
        data['title'] = obj.title
        data['difficult'] = obj.difficult
        data['level'] = obj.level
        data['max_enemys'] = obj.max_enemys
        data['speed'] = obj.speed
        response.set_cookie('data', data, samesite=None, max_age=200)
        return response