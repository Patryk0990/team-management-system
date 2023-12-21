from django.contrib.auth.views import PasswordResetCompleteView
from django.utils.translation import gettext as _


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/users/password_reset/password_reset_complete.html"
    title = _("Password reset complete")
