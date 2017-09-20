from django import forms

from uploads.core.models import Document
from uploads.core.models import InputDocument

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )

class InputDocumentForm(forms.ModelForm):
    class Meta:
        model = InputDocument
        fields = ('idocument',)