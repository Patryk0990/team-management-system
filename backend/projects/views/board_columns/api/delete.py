from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.models import BoardColumn, Task
from utils.mixins.api import APIProjectManagerRequiredMixin


class APIBoardColumnDeleteView(APIProjectManagerRequiredMixin, View):

    def delete(self, request, project_pk, board_pk, pk):
        try:
            board_column = BoardColumn.objects.get(pk=pk, board=board_pk, board__project=project_pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('Board column with this id and project/board relation does not exist.')},
                status=404,
            )

        Task.objects.filter(board_column=board_column).delete()
        board_column.delete()

        return JsonResponse({'message': _('Board column was deleted successfully.')})
