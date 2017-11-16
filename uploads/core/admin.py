from django.contrib import admin
from uploads.core.models import Document
from uploads.core.models import InputDocument
# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('description','document','uploaded_at')
admin.site.register(Document,DocumentAdmin)

class InputDocumentAdmin(admin.ModelAdmin):
    list_display = ('idocument','iuploaded_at')
admin.site.register(InputDocument,InputDocumentAdmin)