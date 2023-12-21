from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.utils.translation import gettext as _
from django.views.generic import View

from projects.forms import ProjectForm
from projects.models import Project, ProjectMember
from utils.bs_form_renderer import BootstrapFormRenderer
from utils.mixins.api import APISuperUserRequiredMixin


class APIProjectModifyView(APISuperUserRequiredMixin, View):
    form_class = ProjectForm
    form_renderer = BootstrapFormRenderer

    def get(self, request, project_pk):
        try:
            project = Project.objects.get(pk=project_pk)
        except ObjectDoesNotExist:
            return HttpResponse(_('Project with this id does not exist.'), status=404)
        rendered_form = self.form_renderer().render(
            self.form_renderer.form_template_name,
            {
                'form': self.form_class(
                    initial={
                        'manager': ProjectMember.objects.get(project=project, role=ProjectMember.Role.MANAGER).user.pk,
                    },
                    instance=project,
                ),
            },
        )

        return HttpResponse(rendered_form)

    def post(self, request, project_pk):
        try:
            project = Project.objects.get(pk=project_pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': _('Project with this id does not exist.')},
                status=404,
            )

        form = self.form_class(request.POST, instance=project)
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
        return JsonResponse({'message': _('Project was modified successfully.')})
