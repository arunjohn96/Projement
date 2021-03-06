from django.conf.urls import url
from django.urls import path

from projects.views import AssignmentView, DashboardView, ProjectUpdateView


urlpatterns = [
    url(r'^$', AssignmentView.as_view(), name='assignment'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^projects/(?P<pk>[0-9]+)-(?P<slug>[-\w]*)/$', ProjectUpdateView.as_view(), name='project-update'),
    path('projects/download_xl/', DashboardView.download_project_xlsx, name='project-xl')
]
