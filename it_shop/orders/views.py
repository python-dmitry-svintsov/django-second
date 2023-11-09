import sys
import math
from django.contrib import messages
from django.utils.translation import gettext_lazy

from django.contrib.auth.models import Group, ContentType

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, View, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


def printing(data):
    print(data, file=sys.stdout)


class CreateOrder(LoginRequiredMixin, View):
    login_url = reverse_lazy('my_auth:login')

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        cart = Cart(request)
        form = OrderCreateForm
        return render(request, 'orders/create.html', context={'cart': cart, 'form': form})

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        message = {}
        mes_ind = 1
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            user = request.user
            order.user = user
            order.save()
            for item in cart:
                currtent_quantity = max(min(item['quantity'], item['product'].quantity), 0)
                OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                item['product'].quantity -= currtent_quantity
                item['product'].save()
                message[f'product{mes_ind}'] = f'К сожалению количество товара ({item["product"].title})' \
                                               f' на складе ограничено' if currtent_quantity < item['quantity'] else ''
                mes_ind += 1
            # очистка корзины
            cart.clear()
            request.session['coupon_id'] = None
            # запуск асинхронной задачи
            order_created.delay(order.id)
            return render(request, 'orders/created.html', context={'order': order, 'message': message})


class Order_Moderator_List(PermissionRequiredMixin, ListView):
    permission_required = tuple(f'{permission.content_type.app_label}.{permission.codename}' for permission in Group.objects.get(name='moderators').permissions.all())
    model = Order
    paginate_by = 100
    template_name = 'orders/order-list.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["oder_item"] = OrderItem.objects.all()
        return context

    def handle_no_permission(self):
        printing(self.permission_required)
        messages.add_message(
            self.request, messages.INFO,
            gettext_lazy('У вас нету прав на просмотр данной страницы')
        )
        return redirect('my_auth:login')


class Order_Detail(PermissionRequiredMixin, DetailView):
    permission_required = tuple(f'{permission.content_type.app_label}.{permission.codename}' for permission in
                                Group.objects.get(name='moderators').permissions.all())
    model = Order
    template_name = 'orders/order-detail.html'
    context_object_name = 'order'