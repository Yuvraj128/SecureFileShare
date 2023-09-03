from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.

def validate_file_mimetype(file):
    """
    This checks the file to be uploaded is allowed or not.
    """
    accepted_files = [
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        ]
    
    if file.content_type not in accepted_files:
        raise ValidationError("Only pptx, docx, and xlsx file are supported.")
    
class Files(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/',validators=[validate_file_mimetype])