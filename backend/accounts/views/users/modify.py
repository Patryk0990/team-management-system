from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import View

from accounts.forms import UserForm
from accounts.models import User
from utils.mixins import AuthRequiredMixin


class UserModifyView(AuthRequiredMixin, View):
    template_name = 'accounts/users/modify.html'
    form_class = UserForm

    def get(self, request, pk):
        context = self.get_context_data()
        if request.user.pk != pk:
            messages.warning(request, _('You are not allowed to edit this account data.'))
            return redirect(reverse('dashboard'))

        try:
            user = User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            messages.error(request, _('User with this id does not exist.'))
            return redirect(reverse('dashboard'))

        context['user_form'] = self.form_class(instance=user)
        return render(request, self.template_name, context=context)

    def post(self, request, pk):
        context = self.get_context_data()

        if request.user.pk != pk:
            messages.warning(request, _('You are not allowed to edit this account data.'))
            return redirect(reverse('dashboard'))

        try:
            user = User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            messages.error(request, _('User with this id does not exist.'))
            return redirect(reverse('dashboard'))

        form = self.form_class(request.POST, instance=user)
        if not form.is_valid():
            context['user_form'] = form
            messages.error(request, form.non_field_errors())
        else:
            form.save()
            context['user_form'] = self.form_class(instance=user)
            messages.success(request, _('Successfully modified your data.'))

        return render(request, self.template_name, context=context)
