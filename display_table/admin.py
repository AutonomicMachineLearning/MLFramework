from django.contrib import admin
from display_table.models import Table

class DisplayTableAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'office', 'age', 'start_date', 'salary')

admin.site.register(Table, DisplayTableAdmin)