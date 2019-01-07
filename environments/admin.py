from django.contrib import admin

# Register your models here.
from environments.models import Environments

class EnvironmentsAdmin(admin.ModelAdmin):
    list_display = ()

admin.site.register(Environments, EnvironmentsAdmin)