from django.forms import ModelForm

from projects.models import ProjectMember


class ModifyProjectMemberForm(ModelForm):
    class Meta:
        model = ProjectMember
        fields = ('role', )

    def __init__(self, *args, **kwargs):
        super(ModifyProjectMemberForm, self).__init__(*args, **kwargs)
        self.fields['role'].choices = [
            (key, value) for key, value in ProjectMember.Role.choices if key != ProjectMember.Role.MANAGER
        ]
