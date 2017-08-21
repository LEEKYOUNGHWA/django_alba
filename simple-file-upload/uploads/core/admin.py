from django.contrib import admin
from uploads.core.models import Document
# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('description','document','uploaded_at')
admin.site.register(Document,DocumentAdmin)