from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.forms import TaskForm, BoardColumnForm
from projects.models import Board
from utils.mixins import ProjectMemberRequiredMixin


class BoardView(ProjectMemberRequiredMixin, View):
    template_name = 'projects/boards/detail.html'
    task_form = TaskForm
    board_column_form = BoardColumnForm

    def get(self, request, project_pk, pk):
        context = self.get_context_data()

        try:
            board = Board.objects.get(pk=pk, project=project_pk)
        except ObjectDoesNotExist:
            messages.error(request, _('Board with this id and project relation does not exist.'))
            return redirect(reverse('dashboard'))

        context['board'] = board
        context['task_form'] = self.task_form(board=board)
        context['board_column_form'] = self.board_column_form()

        return render(request, self.template_name, context=context)
