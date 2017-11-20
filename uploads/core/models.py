from __future__ import unicode_literals

from django.db import models


class SampleFacialDocument(models.Model):
    description = models.CharField(max_length=255, blank=True)
    sdocument = models.FileField(upload_to='sample/facial/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class InputFacialDocument(models.Model):
    idocument = models.FileField(upload_to='userinput/facial/')
    iuploaded_at = models.DateTimeField(auto_now_add=True)

class SampleWDefectDocument(models.Model):
    description = models.CharField(max_length=255, blank=True)
    sdocument = models.FileField(upload_to='sample/weldingdefect/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class InputWDefectDocument(models.Model):
    idocument = models.FileField(upload_to='userinput/weldingdefect/')
    iuploaded_at = models.DateTimeField(auto_now_add=True)