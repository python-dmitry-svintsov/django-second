from django.urls import path
from . import views


urlpatterns = [
    path(r'^create/$', views.CreateOrder.as_view(), name='order_create'),
    path(r'list/', views.Order_Moderator_List.as_view(), name='order-list'),
    path(r'^detail/<int:pk>/$', views.Order_Detail.as_view(), name='order-datail')
]