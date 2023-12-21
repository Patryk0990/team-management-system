from django.contrib import messages
from django.contrib.auth.views import PasswordResetView

from accounts.forms import CustomPasswordResetForm


class CustomPasswordResetView(PasswordResetView):
    email_template_name = "mails/accounts/users/password_reset/password_reset.html"
    subject_template_name = "mails/accounts/users/password_reset/password_reset_subject.txt"
    template_name = "accounts/users/password_reset/password_reset.html"
    form_class = CustomPasswordResetForm

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)
