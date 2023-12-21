from django.forms import ModelForm

from projects.models import ProjectMemberRating


class EvaluateProjectMemberForm(ModelForm):
    class Meta:
        model = ProjectMemberRating
        fields = ('hard_skills', 'soft_skills', 'performance', 'activity')

    def __init__(self, *args, **kwargs):
        self.project_member = kwargs.pop('project_member')
        super(EvaluateProjectMemberForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if commit:
            project_member_rating, created = ProjectMemberRating.objects.update_or_create(
                project_member=self.project_member,
                defaults={
                    'hard_skills': self.cleaned_data.get('hard_skills'),
                    'soft_skills': self.cleaned_data.get('soft_skills'),
                    'performance': self.cleaned_data.get('performance'),
                    'activity': self.cleaned_data.get('activity'),
                },
            )
        else:
            try:
                project_member_rating = ProjectMemberRating.objects.get(project_member=self.project_member)
                project_member_rating.hard_skills = self.cleaned_data.get('hard_skills')
                project_member_rating.soft_skills = self.cleaned_data.get('soft_skills')
                project_member_rating.performance = self.cleaned_data.get('performance')
                project_member_rating.activity = self.cleaned_data.get('activity')
            except ProjectMemberRating.DoesNotExist:
                project_member_rating = ProjectMemberRating(
                    project_member=self.project_member,
                    hard_skills=self.cleaned_data.get('hard_skills'),
                    soft_skills=self.cleaned_data.get('soft_skills'),
                    performance=self.cleaned_data.get('performance'),
                    activity=self.cleaned_data.get('activity'),
                )

        return project_member_rating
