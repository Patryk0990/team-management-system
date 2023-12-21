from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.models import ProjectMember
from utils.mixins.api import APIProjectManagerRequiredMixin


class APIProjectMemberDeleteView(APIProjectManagerRequiredMixin, View):

    def delete(self, request, project_pk, pk):
        try:
            project_member = ProjectMember.objects.get(pk=pk, project=project_pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('Project member with this id and project relation does not exist.')},
                status=404,
            )

        project_member.delete()
        return JsonResponse({'message': _('Project member was deleted successfully.')})
