from pathlib import Path
from time import strftime, localtime

from django.db import models

import uuid


def file_path(instance, filename):
    return '{0}/{1}{2}'.format(strftime('%Y/%m/%d', localtime()), uuid.uuid4(), Path(filename).suffix)


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(blank=False, null=False, upload_to=file_path)
    file_name = models.TextField()

    def __str__(self):
        return self.file_name
