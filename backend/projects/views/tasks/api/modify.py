from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.forms import TaskForm
from projects.models import Task
from utils.bs_form_renderer import BootstrapFormRenderer
from utils.mixins.api import APIProjectMemberRequiredMixin


class APITaskModifyView(APIProjectMemberRequiredMixin, View):
    form_class = TaskForm
    form_renderer = BootstrapFormRenderer

    def get(self, request, project_pk, board_pk, pk):
        try:
            task = Task.objects.get(pk=pk, board_column__board=board_pk, board_column__board__project=project_pk)
        except ObjectDoesNotExist:
            return HttpResponse(_('Task with this id and project/board relation does not exist.'), status=404)

        rendered_form = self.form_renderer().render(
            self.form_renderer.form_template_name,
            {'form': self.form_class(board=task.board_column.board, instance=task)},
        )

        return HttpResponse(rendered_form)

    def post(self, request, project_pk, board_pk, pk):
        try:
            task = Task.objects.get(pk=pk, board_column__board=board_pk, board_column__board__project=project_pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('Task with this id and project/board relation does not exist.')},
                status=404,
            )

        form = self.form_class(request.POST, board=task.board_column.board, instance=task)
        if not form.is_valid():
            return JsonResponse(
                {
                    'message': {
                        'field_errors': dict(form.errors),
                        'non_field_errors': form.non_field_errors(),
                    },
                },
                status=400,
            )
        form.save()
        return JsonResponse({'message': _('Task was modified successfully.')})
