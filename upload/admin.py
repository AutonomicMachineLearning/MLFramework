from django.contrib import admin

from upload.models import Document

# Register your models here.
class CoreAdmin(admin.ModelAdmin):
    list_display = ('description', 'document', 'uploaded_at')

admin.site.register(Document, CoreAdmin)