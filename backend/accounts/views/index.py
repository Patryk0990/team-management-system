from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic import View

from accounts.forms import LoginForm, RegisterForm
from accounts.models import User


class IndexView(View):
    template_name = 'index.html'
    registration_done_template_name = 'accounts/users/registration_done.html'
    login_form = LoginForm
    register_form = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)

    def __handle_login(self, request):
        form = self.login_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if user := authenticate(email=email, password=password):
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            elif User.objects.filter(email=email, is_active=False).exists():
                messages.error(request, _('Account with this e-mail address is not active.'))
            else:
                messages.error(request, _('Invalid e-mail address or password.'))
        else:
            messages.error(request, form.non_field_errors())

        return render(
            request,
            self.template_name,
            context={'login_form': form, 'register_form': self.register_form(), 'active_form': 'login'},
        )

    def __handle_registration(self, request):
        form = self.register_form(request.POST)
        if not form.is_valid():
            messages.error(request, form.non_field_errors())
        else:
            form.save()
            return render(request, self.registration_done_template_name)

        return render(
            request,
            self.template_name,
            context={'login_form': self.login_form(), 'register_form': form, 'active_form': 'register'},
        )

    def get(self, request):
        return render(
            request,
            self.template_name,
            context={'login_form': self.login_form(), 'register_form': self.register_form(), 'active_form': 'login'},
        )

    def post(self, request):
        if request.POST.get('login'):
            return self.__handle_login(request)
        elif request.POST.get('register'):
            return self.__handle_registration(request)
        else:
            return self.get(request)
