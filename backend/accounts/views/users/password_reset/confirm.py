from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.translation import gettext as _


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/users/password_reset/password_reset_confirm.html"
    title = _("Enter new password")

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)
