import sys

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from .models import Lapi


def printing(data):
    print(data, file=sys.stdout)


class Lapi_Main(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        data = {'data': Lapi.objects.order_by('id')}
        return render(request, 'lapi/main.html', context=data)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return HttpResponseRedirect(reverse_lazy('lapi:lapi-game', kwargs={'slug': request.POST.get('level')}))


class Lapi_Game(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'lapi/game.html', context={'slug': kwargs['slug']})


class Get_Data(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        slug = kwargs['slug']
        json_object = {}
        json_object['data'] = Lapi.objects.get(slug=slug)
        return JsonResponse(json_object, safe=False, encoder=DataEncoder)


class DataEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Lapi):
            return {"title": obj.title, 'difficult ': obj.difficult, 'max_enemys': obj.max_enemys, 'speed': obj.speed,
                    'style': obj.style, 'slug': obj.slug, 'map': obj.get_map(), 'background': obj.background.name}
            # return obj.__dict__
        return super().default(obj)
