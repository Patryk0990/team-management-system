from django.contrib.auth.views import PasswordResetDoneView
from django.utils.translation import gettext as _


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/users/password_reset/password_reset_done.html"
    title = _("Password reset sent")
