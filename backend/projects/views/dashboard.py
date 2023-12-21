from datetime import date, timedelta

from django.shortcuts import render
from django.views.generic import View

from projects.models import Task, ProjectMember, TaskComment
from projects.utils import ProjectMemberRatingHelper
from utils.mixins import AuthRequiredMixin


class DashboardView(AuthRequiredMixin, View):
    template_name = 'dashboard.html'

    def get(self, request):
        context = self.get_context_data()

        last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
        start_day_of_prev_month = last_day_of_prev_month.replace(day=1)

        average_ratings = ProjectMemberRatingHelper.get_average_ratings_for_user(request.user)
        number_of_completed_tasks = Task.objects.filter(
            assigned_to__user=request.user,
            is_archived=True,
        ).count()

        number_of_completed_tasks_in_the_last_month = Task.objects.filter(
            assigned_to__user=request.user,
            is_archived=True,
            modified_at__gte=start_day_of_prev_month,
            modified_at__lte=last_day_of_prev_month,
        ).count()

        user_memberships = ProjectMember.objects.filter(user=request.user).select_related('project').order_by('-pk')
        user_projects = [user_membership.project for user_membership in user_memberships]

        recent_comments = TaskComment.objects.filter(
            project_member__project__in=user_projects,
        ).select_related(
            'task',
            'project_member',
        ).order_by('-created_at')[:5]

        assigned_tasks = Task.objects.filter(
            is_archived=False,
            assigned_to__user=request.user,
        ).order_by('-modified_at')[:5]

        completed_tasks = Task.objects.filter(
            is_archived=True,
            assigned_to__user=request.user,
        ).order_by('-modified_at')[:5]

        user_projects = user_projects[:5]

        context['overall_rating'] = average_ratings.overall if average_ratings else 0
        context['number_of_completed_tasks'] = number_of_completed_tasks
        context['number_of_completed_tasks_in_the_last_month'] = number_of_completed_tasks_in_the_last_month
        context['user_projects'] = user_projects
        context['recent_comments'] = recent_comments
        context['assigned_tasks'] = assigned_tasks
        context['completed_tasks'] = completed_tasks

        return render(
            request,
            self.template_name,
            context=context,
        )
