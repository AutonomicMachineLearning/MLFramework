from django.contrib import admin
from projects.models import Projects

class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('projectName', 'projectDescription', 'projectTag', 'cretae_date', 'modify_date', )

admin.site.register(Projects, ProjectsAdmin)