from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.models import Project
from utils.mixins.api import APISuperUserRequiredMixin


class APIProjectDeleteView(APISuperUserRequiredMixin, View):

    def delete(self, request, project_pk):
        try:
            project = Project.objects.get(pk=project_pk)
            project.delete()
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('Project with this id does not exist.')},
                status=404,
            )

        return JsonResponse({'message': _('Project was deleted successfully.')})
