from django.db import models
from django.utils.translation import gettext as _

from accounts.models import User
from .project import Project


class ProjectMember(models.Model):
    class Role(models.TextChoices):
        MANAGER = 'MAN', _('Manager')
        DEVELOPER = 'DEV', _('Developer')
        TESTER = 'TES', _('Tester')

    role = models.CharField(_('role'), max_length=3, choices=Role.choices, default=Role.DEVELOPER)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships', verbose_name=_('user'))
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members', verbose_name=_('project'))

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.get_role_display()}'
