from django.urls import path
from . import views


urlpatterns = [
    path(r'^apply/$', views.Coupon_Apply.as_view(), name='apply'),
]