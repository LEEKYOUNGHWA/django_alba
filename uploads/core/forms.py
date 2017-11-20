from django import forms

from uploads.core.models import SampleFacialDocument
from uploads.core.models import InputFacialDocument
from uploads.core.models import SampleWDefectDocument
from uploads.core.models import InputWDefectDocument

class SampleFacialDocumentForm(forms.ModelForm):
    class Meta:
        model = SampleFacialDocument
        fields = ('sdocument', )

class InputFacialDocumentForm(forms.ModelForm):
    class Meta:
        model = InputFacialDocument
        fields = ('idocument',)

class SampleWDefectDocumentForm(forms.ModelForm):
    class Meta:
        model = SampleWDefectDocument
        fields = ('sdocument', )

class InputWDefectDocumentForm(forms.ModelForm):
    class Meta:
        model = InputWDefectDocument
        fields = ('idocument',)