from django import template

from projects.models import ProjectMember

register = template.Library()


@register.filter
def is_project_manager(user, project):
    if not user.is_active:
        return False

    return user.memberships.filter(project=project, role=ProjectMember.Role.MANAGER).exists()
