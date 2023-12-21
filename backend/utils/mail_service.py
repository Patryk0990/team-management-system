from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from accounts.utils import EmailVerificationTokenGenerator

if TYPE_CHECKING:
    from accounts.models import User


class MailService:

    @staticmethod
    def send_email_verification_mail(user: User) -> dict[str, str]:
        token_generator = EmailVerificationTokenGenerator()
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        url = (
            f'{Site.objects.get_current().domain}'
            f'{reverse("email-verify", kwargs={"uidb64": uidb64, "token": token})}'
        )

        context = {'name': user.first_name, 'site_name': Site.objects.get_current().name, 'url': url}

        subject = render_to_string('mails/accounts/users/email_verify_subject.txt', context)
        html_message = render_to_string('mails/accounts/users/email_verify.html', context)
        plain_message = strip_tags(html_message)

        return MailService.__send_mail(subject, plain_message, html_message, [user.email])

    @staticmethod
    def __send_mail(subject, plain_message, html_message, recipient_list, from_email=None):
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                html_message=html_message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            response = {'status': 'success'}
        except Exception as e:
            response = {'status': 'error', 'detail': str(e)}

        return response
