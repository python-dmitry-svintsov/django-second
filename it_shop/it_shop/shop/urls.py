from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('books/', views.Books.as_view(), name='books'),
    path('books/<int:pk>/', views.Detail_Book.as_view(), name='detail')
]