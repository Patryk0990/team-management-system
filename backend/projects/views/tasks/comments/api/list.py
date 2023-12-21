from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.models import Task, TaskComment
from utils.mixins.api import APIProjectMemberRequiredMixin


class APITaskCommentListView(APIProjectMemberRequiredMixin, View):
    paginate_by = 5
    template_name = 'projects/tasks/comments/list.html'

    def get(self, request, project_pk, board_pk, task_pk):
        try:
            task = Task.objects.get(
                pk=task_pk,
                board_column__board=board_pk,
                board_column__board__project=project_pk,
            )
        except ObjectDoesNotExist:
            return HttpResponse(_('Task with this id and project/board relation does not exist.'), status=404)

        task_comments = TaskComment.objects.filter(task=task).order_by('-created_at')
        if not task_comments.exists():
            return HttpResponse(_('No comments to display.'))

        paginator = Paginator(task_comments, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}

        return render(request, self.template_name, context=context)
