from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.models import Task
from utils.mixins.api import APIProjectMemberRequiredMixin


class APITaskDeleteView(APIProjectMemberRequiredMixin, View):

    def delete(self, request, project_pk, board_pk, pk):
        try:
            task = Task.objects.get(pk=pk, board_column__board=board_pk, board_column__board__project=project_pk)
            task.delete()
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('Task with this id and project/board relation does not exist.')},
                status=404,
            )

        return JsonResponse({'message': _('Task was deleted successfully.')})
