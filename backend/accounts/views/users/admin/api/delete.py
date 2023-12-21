from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from accounts.models import User
from utils.mixins import SuperUserRequiredMixin


class APIUserDeleteView(SuperUserRequiredMixin, View):

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('User with this id does not exist.')},
                status=404,
            )

        return JsonResponse({'message': _('User was deleted successfully.')})
