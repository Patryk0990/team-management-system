from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import View

from accounts.models import User
from projects.models import Task
from projects.utils import ProjectMemberRatingHelper
from utils.mixins import AuthRequiredMixin


class UserProfileView(AuthRequiredMixin, View):
    template_name = 'accounts/users/profile.html'

    def get(self, request, pk):
        context = self.get_context_data()

        try:
            user = User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            messages.error(request, _('User with this id does not exist.'))
            return redirect(reverse('dashboard'))

        number_of_completed_tasks = Task.objects.filter(assigned_to__user=user, is_archived=True).count()
        number_of_completed_tasks_per_project = {}
        for membership in user.memberships.all():
            number_of_completed_tasks_per_project[membership.project.name] = membership.assigned_tasks.filter(
                is_archived=True,
            ).count()
        average_ratings = ProjectMemberRatingHelper.get_average_ratings_for_user(user)

        context['profile_user'] = user
        context['average_ratings'] = average_ratings
        context['number_of_completed_tasks'] = number_of_completed_tasks
        context['number_of_completed_tasks_per_project'] = number_of_completed_tasks_per_project
        return render(request, self.template_name, context=context)
