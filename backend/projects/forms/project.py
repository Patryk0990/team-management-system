from django import forms
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from projects.models import Project, ProjectMember


class ProjectForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label=_('Project manager'))

    class Meta:
        model = Project
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            existing_users_in_project = ProjectMember.objects.filter(project=self.instance.pk).exclude(
                role=ProjectMember.Role.MANAGER,
            ).values_list('user', flat=True)
            self.fields['user'].queryset = User.objects.exclude(pk__in=existing_users_in_project)

    def save(self, commit=True):
        project = super().save(commit)
        user = self.cleaned_data.get('user')

        try:
            ProjectMember.objects.get(project=project, role=ProjectMember.Role.MANAGER).delete()
        except ProjectMember.DoesNotExist:
            pass
        ProjectMember.objects.create(project=project, role=ProjectMember.Role.MANAGER, user=user)

        return project
