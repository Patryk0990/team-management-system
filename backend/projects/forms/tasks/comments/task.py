from django import forms
from django.utils.translation import gettext as _

from projects.models import TaskComment


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('content', )
        labels = {
            'content': _('Write a comment'),
        }

    def __init__(self, *args, **kwargs):
        self.project_member = kwargs.pop('project_member')
        self.task = kwargs.pop('task')

        super(TaskCommentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        task_comment = TaskComment(
            content=self.cleaned_data.get('content'),
            project_member=self.project_member,
            task=self.task,
        )
        if commit:
            task_comment.save()

        return task_comment
