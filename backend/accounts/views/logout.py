from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import View

from utils.mixins import AuthRequiredMixin


class LogoutView(AuthRequiredMixin, View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect(settings.LOGIN_URL)
