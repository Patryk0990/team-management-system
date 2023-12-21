from django.db.models import Avg

from accounts.models import User
from projects.models import ProjectMemberRating
from .project_member_ratings import ProjectMemberAverageRating


class ProjectMemberRatingHelper:
    @staticmethod
    def get_average_ratings_for_user(user: User):
        project_member_rating = ProjectMemberRating.objects.filter(project_member__user=user)
        if not project_member_rating.exists():
            return None

        return ProjectMemberAverageRating(**project_member_rating.aggregate(
            hard_skills=Avg('hard_skills'),
            soft_skills=Avg('soft_skills'),
            performance=Avg('performance'),
            activity=Avg('activity'),
        ))
