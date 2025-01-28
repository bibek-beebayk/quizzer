import os

from django.utils import timezone
from storages.backends.s3boto3 import S3Boto3Storage


class CKEditorR2Storage(S3Boto3Storage):
    location = "ckeditor"

    def get_available_name(self, name, max_length=None):
        # Add timestamp to ensure unique filenames
        now = timezone.now().strftime("%Y%m%d_%H%M%S")
        name_parts = os.path.splitext(name)
        return f"{name_parts[0]}_{now}{name_parts[1]}"
