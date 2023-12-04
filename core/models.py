from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class File(models.Model):
    namefile = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.namefile

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
