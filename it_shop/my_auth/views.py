from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, View
from django.utils.translation import gettext_lazy
from .forms import UserRegisterForm, User_Profile_Update_Form
from .models import Sex
import sys


def printing(data):
    print(data, file=sys.stdout)


class Register_User(SuccessMessageMixin, CreateView):
    template_name = 'my_auth/user_register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('my_auth:login')

    def form_valid(self, form):
        user = form.save()
        try:
            with transaction.atomic():
                group = Group.objects.get(name='costumers')
                user.groups.add(group)
                login(self.request, user)
                messages.add_message(
                    self.request, messages.INFO,
                    gettext_lazy('Вы успешно зарегистрированы! Введите пожалуйста ФИО.')
                )
                return HttpResponseRedirect(reverse_lazy('my_auth:profile', kwargs={'slug': user.slug}))
        except ObjectDoesNotExist:
            messages.add_message(self.request, messages.INFO, gettext_lazy('К сожалению запрос не удался, попробуйте позже!'))
            return HttpResponseRedirect(reverse_lazy('my_auth:register'))
        except IntegrityError:
            messages.add_message(self.request, messages.INFO, gettext_lazy('Вы уже зарегистрированы!'))
            return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        printing(form.errors)
        return HttpResponseRedirect(self.success_url)


class Login_User(SuccessMessageMixin, LoginView):
    template_name = 'my_auth/login.html'

    def form_invalid(self, form):
        messages.add_message(
                self.request, messages.INFO, gettext_lazy('Неверный логин или пароль. Проверьте введённые данные'))
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, gettext_lazy(f'Вы успешно вошли в систему.'))
        return super().form_valid(form)


class Profile_User(PermissionRequiredMixin, DetailView):
    permission_required = 'my_auth.view_myuser'
    login_url = reverse_lazy('my_auth:login')
    model = get_user_model()
    template_name = 'my_auth/profile.html'
    context_object_name = 'profile'


class Logout_User(LogoutView):
    next_page = '/shop/'


class Update_Profile_User(LoginRequiredMixin, SuccessMessageMixin, View):
    login_url = reverse_lazy('my_auth:login')

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        data = get_user_model().objects.get(id=request.user.id)
        sex = Sex.objects.all()
        data = {'profile': data, 'sex': sex}
        return render(request, template_name='my_auth/update_profile.html', context=data)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = request.user
        slug = kwargs['slug']
        form = User_Profile_Update_Form(request.POST, request.FILES, instance=user)
        if form.is_valid():
            delete = request.POST.get('delete_photo')
            if delete:
                user.photo = None
                user.photo.delete(save=True)
                messages.add_message(
                    self.request, messages.INFO, gettext_lazy(f'фотография пользователя {user.username} удалена'))
            messages.add_message(
                self.request, messages.INFO, gettext_lazy(f'данные пользователя {user.username} изменены'))
            form.save()
            return HttpResponseRedirect(reverse_lazy('my_auth:profile', kwargs={'slug': slug}))
        else:
            messages.add_message(
                self.request, messages.INFO, gettext_lazy(f'введенные данные некоректны!'))
            return HttpResponseRedirect(reverse_lazy('my_auth:update-profile', kwargs={'slug': slug}))
