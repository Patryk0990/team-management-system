from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from projects.models import ProjectMember
from utils.mixins import AuthRequiredMixin


class ProjectMemberRequiredMixin(AuthRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            ProjectMember.objects.get(user=request.user, project=kwargs['project_pk'])
        except ObjectDoesNotExist:
            messages.error(request, _('You need to be a member of this project to access this resource.'))
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
