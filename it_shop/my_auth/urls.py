from django.urls import path
from .views import Register_User, Login_User, Profile_User, Logout_User, Update_Profile_User


urlpatterns = [
    path('register/', Register_User.as_view(), name='register'),
    path('login/', Login_User.as_view(), name='login'),
    path('profile/<slug:slug>/', Profile_User.as_view(), name='profile'),
    path('logout', Logout_User.as_view(), name='logout'),
    path('profile/<slug:slug>/update/', Update_Profile_User.as_view(), name='update-profile')
]