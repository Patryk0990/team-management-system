from django.http import HttpResponse
from django.utils.translation import gettext as _

from utils.mixins.api import APIAuthRequiredMixin


class APISuperUserRequiredMixin(APIAuthRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse(_('You need to be a super user to access this resource.'), status=403)
        return super().dispatch(request, *args, **kwargs)
