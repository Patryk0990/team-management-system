from django.db import models
from django.utils.translation import gettext as _


class Project(models.Model):
    name = models.CharField(_('name'), max_length=64)
    description = models.TextField(_('description'))

    def __str__(self):
        return _(self.name)
