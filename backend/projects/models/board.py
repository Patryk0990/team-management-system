from django.db import models
from django.utils.translation import gettext as _

from .project import Project


class Board(models.Model):
    name = models.CharField(_('name'), max_length=64)
    project = models.ForeignKey(Project, on_delete=models.RESTRICT, related_name='boards', verbose_name=_('project'))

    def __str__(self):
        return _(self.name)
