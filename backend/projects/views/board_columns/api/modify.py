from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.forms import BoardColumnForm
from projects.models import BoardColumn
from utils.bs_form_renderer import BootstrapFormRenderer
from utils.mixins.api import APIProjectManagerRequiredMixin


class APIBoardColumnModifyView(APIProjectManagerRequiredMixin, View):
    form_class = BoardColumnForm
    form_renderer = BootstrapFormRenderer

    def get(self, request, project_pk, board_pk, pk):
        try:
            board_column = BoardColumn.objects.get(pk=pk, board=board_pk, board__project=project_pk)
        except ObjectDoesNotExist:
            return HttpResponse(_('Board column with this id and project/board relation does not exist.'), status=404)

        rendered_form = self.form_renderer().render(
            self.form_renderer.form_template_name,
            {'form': self.form_class(instance=board_column)},
        )

        return HttpResponse(rendered_form)

    def post(self, request, project_pk, board_pk, pk):
        try:
            board_column = BoardColumn.objects.get(pk=pk, board=board_pk, board__project=project_pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('Board column with this id and project/board relation does not exist.')},
                status=404,
            )

        form = self.form_class(request.POST, instance=board_column)
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
        form.save()
        return JsonResponse({'message': _('Board column was modified successfully.')})
