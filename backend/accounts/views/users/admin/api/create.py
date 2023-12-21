from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from accounts.forms import RegisterForm
from utils.mixins import SuperUserRequiredMixin


class APIUserCreateView(SuperUserRequiredMixin, View):
    form_class = RegisterForm

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
        return JsonResponse({'message': _('User was created successfully.')}, status=201)
