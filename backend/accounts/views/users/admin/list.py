from django.shortcuts import render
from django.views.generic import View

from accounts.forms import RegisterForm
from accounts.models import User
from utils.mixins import SuperUserRequiredMixin


class UserListView(SuperUserRequiredMixin, View):
    template_name = 'accounts/users/admin/list.html'
    form_class = RegisterForm

    def get(self, request):
        context = self.get_context_data()
        context['users'] = User.objects.all().order_by('pk')
        context['user_form'] = self.form_class()

        return render(request, self.template_name, context=context)
