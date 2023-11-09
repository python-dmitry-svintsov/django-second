from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView
from django.http import HttpRequest, HttpResponse
from .models import Categories, It_Book
from cart.forms import Product_Add_Form
import sys


def printing(data):
    print(data, file=sys.stdout)


class Home(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        data = {}
        data['categories'] = Categories.objects.all()
        return render(request, 'shop/home.html', context=data)


class Books(ListView):
    paginate_by = 40
    model = It_Book
    context_object_name = 'books'
    template_name = 'shop/books.html'


class Detail_Book(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('my_auth:login')
    model = It_Book
    template_name = 'shop/detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super(Detail_Book, self).get_context_data(**kwargs)
        context['form'] = Product_Add_Form()
        return context

    # def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
    #     data = It_Book.objects.get(pk=kwargs['pk'])
    #     form = Product_Add_Form()
    #     return render(request, 'shop/detail.html', context={'book': data, 'form': form})