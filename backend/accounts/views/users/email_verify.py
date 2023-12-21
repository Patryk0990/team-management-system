from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.views.generic import View

from accounts.models import User
from accounts.utils import EmailVerificationTokenGenerator


class EmailVerifyView(View):
    template_name = 'accounts/users/email_verify.html'

    def get(self, request, uidb64=None, token=None):
        uid = urlsafe_base64_decode(uidb64).decode()
        token_generator = EmailVerificationTokenGenerator()
        user = User.objects.get(pk=uid)

        if not user:
            messages.warning(request, _('Invalid link'))

        elif user.is_active or not token_generator.check_token(user, token):
            messages.warning(request, _('Link is no longer valid'))

        else:
            user.is_active = True
            user.save()

            return render(
                request,
                self.template_name,
                context={
                    'return_url': request.build_absolute_uri(reverse('index')),
                },
            )

        return redirect('index')
