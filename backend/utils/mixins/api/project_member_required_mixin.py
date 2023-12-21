from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.translation import gettext as _

from projects.models import ProjectMember
from utils.mixins.api import APIAuthRequiredMixin


class APIProjectMemberRequiredMixin(APIAuthRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            ProjectMember.objects.get(user=request.user, project=kwargs['project_pk'])
        except ObjectDoesNotExist:
            return HttpResponse(_('You need to be a member of this project to access this resource.'), status=403)
        return super().dispatch(request, *args, **kwargs)
