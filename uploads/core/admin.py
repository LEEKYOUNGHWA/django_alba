from django.contrib import admin

from uploads.core.models import SampleFacialDocument
from uploads.core.models import InputFacialDocument
from uploads.core.models import SampleWDefectDocument
from uploads.core.models import InputWDefectDocument
# Register your models here.
class SampleFacialDocumentAdmin(admin.ModelAdmin):
    list_display = ('sdocument','uploaded_at')
admin.site.register(SampleFacialDocument, SampleFacialDocumentAdmin)

class InputFacialDocumentAdmin(admin.ModelAdmin):
    list_display = ('idocument','iuploaded_at')
admin.site.register(InputFacialDocument,InputFacialDocumentAdmin)

class SampleWDefectDocumentAdmin(admin.ModelAdmin):
    list_display = ('sdocument','uploaded_at')
admin.site.register(SampleWDefectDocument, SampleWDefectDocumentAdmin)

class InputWDefectDocumentAdmin(admin.ModelAdmin):
    list_display = ('idocument','iuploaded_at')
admin.site.register(InputWDefectDocument,InputWDefectDocumentAdmin)