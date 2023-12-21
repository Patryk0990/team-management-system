from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.forms import BoardColumnForm
from projects.models import Board
from utils.mixins.api import APIProjectManagerRequiredMixin


class APIBoardColumnCreateView(APIProjectManagerRequiredMixin, View):
    form_class = BoardColumnForm

    def post(self, request, project_pk, board_pk):
        try:
            board = Board.objects.get(pk=board_pk, project=project_pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('Board with this id and project relation does not exist.')},
                status=404,
            )

        form = self.form_class(request.POST)
        if not form.is_valid():
            return JsonResponse(
                {
                    'message': {
                        'field_errors': dict(form.errors),
                        'non_field_errors': form.non_field_errors(),
                    },
                },
                status=400
            )

        instance = form.save(commit=False)
        instance.board = board
        instance.save()

        return JsonResponse({'message': _('Board column was created successfully.')}, status=201)
