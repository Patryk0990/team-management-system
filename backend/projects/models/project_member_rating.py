from django.db import models
from django.utils.translation import gettext as _

from .project_member import ProjectMember


class ProjectMemberRating(models.Model):
    class Rating(models.IntegerChoices):
        BAD = 1, _('Bad')
        INSUFFICIENT = 2, _('Insufficient')
        SATISFACTORY = 3, _('Satisfactory')
        GOOD = 4, _('Good')
        EXCELLENT = 5, _('Excellent')

    hard_skills = models.PositiveSmallIntegerField(_('hard skills'), choices=Rating.choices)
    soft_skills = models.PositiveSmallIntegerField(_('soft skills'), choices=Rating.choices)
    performance = models.PositiveSmallIntegerField(_('performance'), choices=Rating.choices)
    activity = models.PositiveSmallIntegerField(_('activity'), choices=Rating.choices)
    project_member = models.OneToOneField(
        ProjectMember, on_delete=models.CASCADE, related_name='rating', verbose_name=_('project member'),
    )

    @property
    def overall(self):
        return round(
            (self.hard_skills + self.soft_skills + self.performance + self.activity) / 4,
            2,
        )

    def __str__(self):
        return (
            f'{self.overall} {_("rating for")} {self.project_member.user} {_("for the")} '
            f'{self.project_member.project}'
        )
