from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import View, DetailView, UpdateView, CreateView
from django.http import HttpRequest, HttpResponse, QueryDict, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.views import LogoutView, LoginView
from .models import MyUser, Sex
from django.contrib.auth.models import Group, Permission
from django.db import transaction
from django.db.utils import IntegrityError
import sys


def printing(data):
    print(data, file=sys.stdout)


class Log_view(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        authenticated = True if request.user.is_authenticated else False
        return render(request, 'my_auth/log_in.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/shop')
        else:
            return render(request, 'my_auth/log_in.html', context={'error': True})


class UserLogin(SuccessMessageMixin, LoginView):
    template_name = 'my_auth/log_in.html'

    def form_invalid(self, form):
        """Отправляем сообщение пользователю о неверных данных"""
        messages.add_message(
            self.request, messages.INFO, gettext_lazy('Неверный логин или пароль. Проверьте введённые данные'))
        return super().form_invalid(form)


class Profile_Detail(DetailView):
    model = MyUser
    template_name = 'my_auth/profile.html'
    context_object_name = 'profile'


class Profile_Update(UpdateView):
    model = MyUser
    form_class = UserForm
    template_name = 'my_auth/update.html'
    context_object_name = 'profile'
    # success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sex'] = Sex.objects.all()
        return context

    def form_valid(self, form):
        responce = super().form_valid(form)
        return responce


class ProfileCreate(CreateView):
    # form_class = UserForm
    template_name = 'my_auth/user_register.html'
    model = MyUser

    def form_valid(self, form):
        user = MyUser.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'],
                                          first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                                          sex=form.cleaned_data['sex'], foto=form.cleaned_data['foto'], city=form.cleaned_data['city'])
        group = Group.objects.get(name='clients')
        pemission_update = Permission.objects.get(codename='change_myuser')
        user.user_permissions.add(pemission_update)
        user.save()
        group.user_set.add(user)
        printing(user.user_permissions.all())
        login(request=self.request, user=user)
        return redirect('/shop/')


class Custumers_Register(SuccessMessageMixin, CreateView):
    # form_class = UserForm
    template_name = 'my_auth/user_register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """После регистрации, пользователю добавляется группа с разрешениями "покупатель"."""
        user = form.save()
        try:
            with transaction.atomic():
                group = Group.objects.get(name='clients')
                user.groups.add(group)
                login(self.request, user)
                messages.add_message(
                    self.request, messages.INFO,
                    gettext_lazy('Вы успешно зарегистрированы!')
                )
                return HttpResponseRedirect(reverse('profile', kwargs={'slug': user.slug}))
        except ObjectDoesNotExist:
            messages.add_message(self.request, messages.INFO, gettext_lazy('К сожалению запрос не удался, попробуйте позже!'))
            return HttpResponseRedirect(reverse('profile-register'))
        except IntegrityError:
            messages.add_message(self.request, messages.INFO, gettext_lazy('Вы уже зарегистрированы!'))
            return HttpResponseRedirect(self.success_url)


class Profile_logout(LogoutView):
    next_page = '/shop/'


# 'class UserForm1(djform.ModelForm):
#     class Meta:
#         model = models.MyUser
#         fields = ['username', 'first_name', 'last_name', 'password', 'city', 'sex', 'foto']
#         sex = djform.ModelChoiceField(label='пол', widget=djform.RadioSelect, queryset=Sex.objects.all())
#         foto = djform.ImageField(widget=djform.ClearableFileInput)
#         widgets = {
#             'username': djform.TextInput(attrs={
#                 'class': 'input-elem',
#                 'placeholder': 'username'
#             }),
#             'first_name': djform.TextInput(attrs={
#                 'class': 'input-elem',
#                 'placeholder': 'имя пользователя'
#             }),
#             'last_name': djform.TextInput(attrs={
#                 'class': 'input-elem',
#                 'placeholder': 'фамилия пользователя'
#             }),
#             'password': djform.PasswordInput(attrs={
#                 'class': 'input-elem',
#                 'placeholder': 'пароль'
#             }),
#             'city': djform.TextInput(attrs={
#                 'class': 'input-elem',
#                 'placeholder': 'город'
#             }),
#
#         }
#
#
#         <fieldset class="field_set">
#             <span class="legend">{{ form.sex.label }} :</span>
#             {% for radio in form.sex %}
#                 <label for="sex{{ loop.index }}">
#                     <span class="radio">{{ radio.choice_label }}</span>
#                     <input id="sex{{ loop.index }}" name="sex" type="radio" value="{{ loop.index }}">
#                 </label>
#             {% endfor %}
#         </fieldset>
#         <div class="image-upload ">
#             {{ form.foto }}
#         </div>

