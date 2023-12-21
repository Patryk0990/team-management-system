from django.db import models
from django.utils.translation import gettext as _

from .task import Task
from .project_member import ProjectMember


class TaskComment(models.Model):
    content = models.CharField(_('content'), max_length=500)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    project_member = models.ForeignKey(ProjectMember, on_delete=models.RESTRICT, verbose_name=_('project member'))
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name=_('task'))

    def __str__(self):
        return f'{self.content} - {self.project_member} {_("at")} {self.created_at}'
