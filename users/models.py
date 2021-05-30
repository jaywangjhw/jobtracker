
from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		default=1
		)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()

    def __str__(self):
        return f'{self.upload.name}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
