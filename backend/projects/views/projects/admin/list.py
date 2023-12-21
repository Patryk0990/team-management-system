from django.shortcuts import render
from django.views.generic import View

from projects.forms import ProjectForm
from projects.models import Project
from utils.mixins import SuperUserRequiredMixin


class ProjectListView(SuperUserRequiredMixin, View):
    template_name = 'projects/projects/admin/list.html'
    form_class = ProjectForm

    def get(self, request):
        context = self.get_context_data()
        context['projects'] = Project.objects.all().order_by('pk')
        context['project_form'] = self.form_class()

        return render(request, self.template_name, context=context)
