from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.forms import BoardForm, CreateProjectMemberForm
from projects.models import Project, BoardColumn
from utils.mixins import ProjectMemberRequiredMixin


class ProjectView(ProjectMemberRequiredMixin, View):
    template_name = 'projects/projects/detail.html'
    board_form = BoardForm
    project_member_form = CreateProjectMemberForm

    def get(self, request, project_pk):
        context = self.get_context_data()

        try:
            project = Project.objects.get(pk=project_pk)
        except ObjectDoesNotExist:
            messages.error(request, _('Project with this id does not exist.'))
            return redirect(reverse('dashboard'))

        user_tasks = request.user.memberships.get(project=project).assigned_tasks.filter(
            board_column__in=BoardColumn.objects.filter(board__project=project), is_archived=False,
        ).order_by('-modified_at')

        context['project'] = project
        context['user_tasks'] = user_tasks
        context['board_form'] = self.board_form()
        context['project_member_form'] = self.project_member_form(project=project)

        return render(request, self.template_name, context=context)
