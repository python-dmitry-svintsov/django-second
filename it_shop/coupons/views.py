from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.utils import timezone

from .forms import CouponApplyForm
from .models import Coupon


class Coupon_Apply(LoginRequiredMixin, View):
    login_url = reverse_lazy('my_auth:login')

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        now = timezone.now()
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__iexact=code,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True)
                request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExists:
                request.session['coupon_id'] = None
        return redirect('cart:cart_detail')