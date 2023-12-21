from django.http import HttpResponse
from django.utils.translation import gettext as _


class AJAXRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return HttpResponse(_('Invalid Request'), status=400)
        return super().dispatch(request, *args, **kwargs)
