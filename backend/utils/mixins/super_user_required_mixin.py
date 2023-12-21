from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from utils.mixins import AuthRequiredMixin


class SuperUserRequiredMixin(AuthRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, _('You need to be a super user to access this resource.'))
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
