from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.forms import ProjectForm
from utils.mixins.api import APISuperUserRequiredMixin


class APIProjectCreateView(APISuperUserRequiredMixin, View):
    form_class = ProjectForm

    def post(self, request):
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

        form.save()
        return JsonResponse({'message': _('Project was created successfully.')}, status=201)
