from django.forms import ModelForm

from accounts.models import User
from projects.models import ProjectMember


class CreateProjectMemberForm(ModelForm):
    class Meta:
        model = ProjectMember
        fields = ('user', 'role')

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project')
        super(CreateProjectMemberForm, self).__init__(*args, **kwargs)

        existing_users_in_project = ProjectMember.objects.filter(project=project).values_list('user__pk', flat=True)
        self.fields['user'].queryset = User.objects.exclude(pk__in=existing_users_in_project)
        self.fields['role'].choices = [
            (key, value) for key, value in ProjectMember.Role.choices if key != ProjectMember.Role.MANAGER
        ]
