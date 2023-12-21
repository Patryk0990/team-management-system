from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.views.generic.base import ContextMixin

from projects.models import Project


class AuthRequiredMixin(LoginRequiredMixin, ContextMixin):
    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You need to be authenticated to access this page.'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = Project.objects.filter(members__user=self.request.user)

        context['user_projects'] = projects
        return context
