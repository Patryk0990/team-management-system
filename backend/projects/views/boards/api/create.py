from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.forms import BoardForm
from projects.models import Project
from utils.mixins.api import APIProjectManagerRequiredMixin


class APIBoardCreateView(APIProjectManagerRequiredMixin, View):
    form_class = BoardForm

    def post(self, request, project_pk):
        try:
            project = Project.objects.get(pk=project_pk)
        except ObjectDoesNotExist:
            return JsonResponse({'message': _('Project with this id does not exist.')}, status=404)

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
        instance.project = project
        instance.save()

        return JsonResponse({'message': _('Board was created successfully.')}, status=201)
