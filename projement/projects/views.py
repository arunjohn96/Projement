import os
from collections import OrderedDict
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from io import BytesIO
from markdown import markdown
from pyexcel_xls import save_data
from projects.forms import ProjectForm
from projects.models import Project
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


class AssignmentView(TemplateView):
    template_name = 'projects/assignment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with open(os.path.join(os.path.dirname(settings.BASE_DIR), 'README.md'), encoding='utf-8') as f:
            assignment_content = f.read()

        context.update({
            'assignment_content': mark_safe(markdown(assignment_content))
        })

        return context


class DashboardView(LoginRequiredMixin, ListView):
    model = Project
    ordering = ('-end_date',)
    context_object_name = 'projects'
    template_name = 'projects/dashboard.html'

    def get_queryset(self):
        projects = super().get_queryset()
        projects = projects.select_related('company')
        projects = sorted(projects, key=lambda m: (m.has_ended,))

        return projects

    def download_project_xlsx(self):
        try:
            projects = Project.objects.all()

        except ObjectDoesNotExist:
            return HttpResponse(' Something went wrong!')

        projects = projects.values(
            'id', 'company', 'title', 'start_date', 'end_date', 'estimated_design',
            'actual_design', 'estimated_development', 'actual_development',
            'estimated_testing', 'actual_testing'
        ).order_by('id')
        data = OrderedDict()
        sheet_data = {"Projects": [
            ['SNo', 'ID', 'company', 'title', 'start_date', 'end_date', 'estimated_design',
             'actual_design', 'estimated_development', 'actual_development',
             'estimated_testing', 'actual_testing']]}
        i = 1
        for project in projects:
            project_details = {}
            project_details['data'] = [i, project['id'], project['company'],
                                       project['title'], project['start_date'], project['end_date'],
                                       project['estimated_design'], project['actual_design'],
                                       project['estimated_development'], project['actual_development'],
                                       project['estimated_testing'], project['actual_testing']]
            sheet_data['Projects'].append(project_details['data'])
            i += 1
        data.update(sheet_data)
        io = BytesIO()
        save_data(io, data)
        io.seek(0)
        response = HttpResponse(
            io.read(), content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ProjectData.xls"'
        return response


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    initial = {}
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        project = form.save(commit=False)
        project.actual_design = project.actual_design + self.get_object().actual_design
        project.actual_testing = project.actual_testing + self.get_object().actual_testing
        project.actual_development = project.actual_development + \
            self.get_object().actual_development
        return super(ProjectUpdateView, self).form_valid(form)
