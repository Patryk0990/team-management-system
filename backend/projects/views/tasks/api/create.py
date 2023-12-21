from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.forms import TaskForm
from projects.models import Board
from utils.mixins.api import APIProjectMemberRequiredMixin


class APITaskCreateView(APIProjectMemberRequiredMixin, View):
    form_class = TaskForm

    def post(self, request, project_pk, board_pk):
        try:
            board = Board.objects.get(pk=board_pk, project=project_pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('Board with this id and project relation does not exist.')},
                status=404,
            )

        form = self.form_class(request.POST, board=board)
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
        try:
            project_member = self.request.user.memberships.get(project=instance.board_column.board.project)
        except ObjectDoesNotExist:
            return JsonResponse({'message': _('User is not a member in this project.')}, status=403)

        instance.created_by = project_member
        instance.save()
        return JsonResponse({'message': _('Task was created successfully.')}, status=201)
