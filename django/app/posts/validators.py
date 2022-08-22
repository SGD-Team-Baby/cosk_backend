from django.core.exceptions import ValidationError 

def validateContentType(value):
    types = ["text", "image", "code", "error"]
    if value not in types:
        raise ValidationError("Type Error")