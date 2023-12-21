from django.db import models
from django.utils.translation import gettext as _

from .board_column import BoardColumn
from .project_member import ProjectMember


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = 'L', _('Low')
        MEDIUM = 'M', _('Medium')
        HIGH = 'H', _('High')

    name = models.CharField(_('name'), max_length=64)
    description = models.TextField(_('description'))
    priority = models.CharField(_('priority'), max_length=1, choices=Priority.choices, default=Priority.LOW)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('modified at'), auto_now=True)
    is_archived = models.BooleanField(_('is archived'), default=False)
    board_column = models.ForeignKey(
       BoardColumn, on_delete=models.RESTRICT, related_name='tasks', verbose_name=_('board column')
    )
    created_by = models.ForeignKey(
        ProjectMember, on_delete=models.SET_NULL, related_name='created_tasks', verbose_name=_('created by'),
        null=True,
    )
    assigned_to = models.ForeignKey(
        ProjectMember, on_delete=models.SET_NULL, related_name='assigned_tasks', verbose_name=_('assigned to'),
        null=True, blank=True,
    )
    comments = models.ManyToManyField(
        to=ProjectMember,
        through='TaskComment',
        through_fields=('task', 'project_member'),
        related_name='comments',
    )

    def __str__(self):
        return _(self.name)
