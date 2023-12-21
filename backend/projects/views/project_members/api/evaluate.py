from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.forms import EvaluateProjectMemberForm
from projects.models import ProjectMember
from utils.bs_form_renderer import BootstrapFormRenderer
from utils.mixins.api import APIProjectManagerRequiredMixin


class APIProjectMemberEvaluateView(APIProjectManagerRequiredMixin, View):
    form_class = EvaluateProjectMemberForm
    form_renderer = BootstrapFormRenderer

    def get(self, request, project_pk, pk):
        try:
            project_member = ProjectMember.objects.select_related('rating').get(pk=pk, project=project_pk)
        except ObjectDoesNotExist:
            return HttpResponse(_('Project member with this id and project relation does not exist.'), status=404)

        try:
            project_member_rating = project_member.rating
        except ProjectMember.rating.RelatedObjectDoesNotExist:
            project_member_rating = None

        rendered_form = self.form_renderer().render(
            self.form_renderer.form_template_name,
            {'form': self.form_class(instance=project_member_rating, project_member=project_member)},
        )

        return HttpResponse(rendered_form)

    def post(self, request, project_pk, pk):
        try:
            project_member = ProjectMember.objects.select_related('rating').get(pk=pk, project=project_pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('Project member with this id and project relation does not exist.')},
                status=404,
            )

        try:
            project_member_rating = project_member.rating
        except ProjectMember.rating.RelatedObjectDoesNotExist:
            project_member_rating = None

        form = self.form_class(request.POST, instance=project_member_rating, project_member=project_member)
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
        return JsonResponse({'message': _('Project member was evaluated successfully.')})
