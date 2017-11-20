from __future__ import unicode_literals

from django.db import models
from easy_thumbnails import fields


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = fields.ThumbnailerField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class InputDocument(models.Model):
    idocument = models.FileField(upload_to='userinputs/')
    iuploaded_at = models.DateTimeField(auto_now_add=True)