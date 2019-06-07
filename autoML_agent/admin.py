from django.contrib import admin
from autoML_agent.models import Table

class ModelingAdmin(admin.ModelAdmin):
    list_display = ()

admin.site.register(Table, ModelingAdmin)