from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from projects.models import Company, Project, Tags


class ProjectAdmin(SimpleHistoryAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date')
    list_filter = ('company','tags')
    ordering = ('-start_date',)

    fieldsets = (
        (None, {'fields': ['company', 'title', 'start_date', 'end_date']}),
        ('Estimated hours', {'fields': ['estimated_design', 'estimated_development', 'estimated_testing']}),
        ('Actual hours', {'fields': ['actual_design', 'actual_development', 'actual_testing']}),
        ('Tag', {'fields': ['tags']}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()

        return 'company',


admin.site.register(Company, SimpleHistoryAdmin)
admin.site.register(Tags, SimpleHistoryAdmin)
admin.site.register(Project, ProjectAdmin)
# register(Company)
# register(Project)
# register(Tags)
