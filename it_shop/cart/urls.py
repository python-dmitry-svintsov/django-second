from django.urls import path
from . import views


urlpatterns = [
    path(r'^$', views.Cart_Detail.as_view(), name='cart_detail'),
    path(r'^add/(?P<product_id>\d+)/$', views.Cart_Add.as_view(), name='cart_add'),
    path(r'^remove/(?P<product_id>\d+)/$', views.Cart_Remove.as_view(), name='cart_remove'),
]