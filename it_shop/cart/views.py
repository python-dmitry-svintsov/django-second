from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, View
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy

from coupons.forms import CouponApplyForm
from shop.models import It_Book
from .cart import Cart
from .forms import Product_Add_Form


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(It_Book, id=product_id)
    form = Product_Add_Form(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=int(cd['quantity']),
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


class Cart_Add(SuccessMessageMixin, LoginRequiredMixin, View):
    login_url = reverse_lazy('my_auth:login')

    def post(self, request: HttpRequest, product_id) -> HttpResponse:
        cart = Cart(request)
        product = get_object_or_404(It_Book, id=product_id)
        form = Product_Add_Form(request.POST)
        if form.is_valid():
            messages.add_message(
                self.request, messages.INFO,
                gettext_lazy(f'Товар "{product.title[:24]}..." успешно добавлен в корзину')
            )
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=int(cd['quantity']),
                     update_quantity=cd['update'])
        return redirect('cart:cart_detail')


class Cart_Remove(SuccessMessageMixin, LoginRequiredMixin, View):
    login_url = reverse_lazy('my_auth:login')

    def get(self, request: HttpRequest, product_id) -> HttpResponse:
        cart = Cart(request)
        product = get_object_or_404(It_Book, id=product_id)
        cart.remove(product)
        messages.add_message(
            self.request, messages.INFO,
            gettext_lazy(f'Товар "{product.title[:24]}..." удален')
        )
        return redirect('cart:cart_detail')


class Cart_Detail(SuccessMessageMixin, LoginRequiredMixin, View):
    login_url = reverse_lazy('my_auth:login')

    def get(self, request: HttpRequest) -> HttpResponse:
        cart = Cart(request)

        for item in cart:
            item['update_quantity_form'] = Product_Add_Form(
                initial={'quantity': item['quantity'],
                         'update': True})
        coupon_apply_form = CouponApplyForm()
        messages.add_message(
            self.request, messages.INFO,
            gettext_lazy(f'ваша корзина состоит из {cart.__len__()} товаров:')
        )
        return render(request, 'cart/detail.html', {'cart': cart, 'form': coupon_apply_form})
        # return render(request, 'cart/detail.html', {'cart': cart})