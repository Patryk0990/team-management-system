from django.http import HttpResponse
from django.utils.translation import gettext as _

from utils.mixins.api import AJAXRequiredMixin


class APIAuthRequiredMixin(AJAXRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(_('You need to be authenticated to access this resource.'), status=401)
        return super().dispatch(request, *args, **kwargs)
