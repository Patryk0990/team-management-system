from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.forms import BoardForm
from projects.models import Board
from utils.bs_form_renderer import BootstrapFormRenderer
from utils.mixins.api import APIProjectManagerRequiredMixin


class APIBoardModifyView(APIProjectManagerRequiredMixin, View):
    form_class = BoardForm
    form_renderer = BootstrapFormRenderer

    def get(self, request, project_pk, pk):
        try:
            board = Board.objects.get(pk=pk, project=project_pk)
        except ObjectDoesNotExist:
            return HttpResponse(_('Board with this id and project relation does not exist.'), status=404)

        rendered_form = self.form_renderer().render(
            self.form_renderer.form_template_name,
            {'form': self.form_class(instance=board)},
        )

        return HttpResponse(rendered_form)

    def post(self, request, project_pk, pk):
        try:
            board = Board.objects.get(pk=pk, project=project_pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('Board with this id and project relation does not exist.')},
                status=404,
            )

        form = self.form_class(request.POST, instance=board)
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
        return JsonResponse({'message': _('Board was modified successfully.')})
