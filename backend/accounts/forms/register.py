from django.contrib.auth.forms import UserCreationForm

from accounts.models import User
from utils import MailService


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()

            if not MailService.send_email_verification_mail(user):
                user.delete()
                return None

            return user
