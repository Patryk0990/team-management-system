from django.db import models
from django.utils.translation import gettext as _

from .board import Board


class BoardColumn(models.Model):
    name = models.CharField(_('name'), max_length=64)
    board = models.ForeignKey(Board, on_delete=models.RESTRICT, related_name='columns', verbose_name=_('board'))

    def __str__(self):
        return _(self.name)
