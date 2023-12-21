from django.shortcuts import render
from django.views.generic import View

from utils.mixins import AuthRequiredMixin


class DashboardView(AuthRequiredMixin, View):
    template_name = 'dashboard.html'

    def get(self, request):

        return render(
            request,
            self.template_name,
            context={},
        )
