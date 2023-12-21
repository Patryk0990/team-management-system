from django import forms

from projects.models import Task, ProjectMember, BoardColumn


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'priority', 'board_column', 'assigned_to')

    def __init__(self, *args, **kwargs):
        board = kwargs.pop('board')

        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = ProjectMember.objects.filter(project=board.project)
        self.fields['board_column'].queryset = BoardColumn.objects.filter(board=board)
