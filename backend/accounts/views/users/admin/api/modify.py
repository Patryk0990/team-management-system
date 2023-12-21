from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from accounts.forms import AdminUserForm
from accounts.models import User
from utils.bs_form_renderer import BootstrapFormRenderer
from utils.mixins import SuperUserRequiredMixin


class APIUserModifyView(SuperUserRequiredMixin, View):
    form_class = AdminUserForm
    form_renderer = BootstrapFormRenderer

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(_('User with this id does not exist.'), status=404)
        rendered_form = self.form_renderer().render(
            self.form_renderer.form_template_name,
            {
                'form': self.form_class(instance=user),
            },
        )

        return HttpResponse(rendered_form)

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('User with this id does not exist.')},
                status=404,
            )

        form = self.form_class(request.POST, request.FILES, instance=user)
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
        return JsonResponse({'message': _('User was modified successfully.')})
