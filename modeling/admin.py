from django.contrib import admin
from modeling.models import Table

class ModelingAdmin(admin.ModelAdmin):
    list_display = ()

admin.site.register(Table, ModelingAdmin)