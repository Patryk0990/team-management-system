from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.forms import TaskCommentForm
from projects.models import Task, ProjectMember
from utils.bs_form_renderer import BootstrapFormRenderer
from utils.mixins.api import APIProjectMemberRequiredMixin


class APITaskCommentCreateView(APIProjectMemberRequiredMixin, View):
    form_class = TaskCommentForm
    form_renderer = BootstrapFormRenderer

    def get(self, request, project_pk, board_pk, task_pk):
        try:
            project_member = ProjectMember.objects.get(user=request.user, project=project_pk)
        except ObjectDoesNotExist:
            return HttpResponse(_('You are not a member of this project.'), status=404)

        try:
            task = Task.objects.get(pk=task_pk, board_column__board=board_pk, board_column__board__project=project_pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('Task with this id and project/board relation does not exist.')},
                status=404,
            )

        rendered_form = self.form_renderer().render(
            self.form_renderer.form_template_name,
            {'form': self.form_class(project_member=project_member, task=task)},
        )

        return HttpResponse(rendered_form)

    def post(self, request, project_pk, board_pk, task_pk):
        try:
            project_member = ProjectMember.objects.get(user=request.user, project=project_pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('You are not a member of this project.')},
                status=404,
            )
        try:
            task = Task.objects.get(pk=task_pk, board_column__board=board_pk, board_column__board__project=project_pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('Task with this id and project/board relation does not exist.')},
                status=404,
            )

        form = self.form_class(request.POST, project_member=project_member, task=task)
        if not form.is_valid():
            return JsonResponse(
                {
                    'message': {
                        'field_errors': dict(form.errors),
                        'non_field_errors': form.non_field_errors(),
                    },
                },
                status=400
            )

        form.save()
        return JsonResponse({'message': _('Comment was created successfully.')}, status=201)
