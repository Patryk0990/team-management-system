from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.models import Board, BoardColumn, Task
from utils.mixins.api import APIProjectManagerRequiredMixin


class APIBoardDeleteView(APIProjectManagerRequiredMixin, View):

    def delete(self, request, project_pk, pk):
        try:
            board = Board.objects.get(pk=pk, project=project_pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('Board with this id and project relation does not exist.')},
                status=404,
            )

        Task.objects.filter(board_column__board=board).delete()
        BoardColumn.objects.filter(board=board).delete()
        board.delete()

        return JsonResponse({'message': _('Board was deleted successfully.')})
