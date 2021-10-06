from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default="", null=True, upload_to='profile_pics')
    real_name = models.CharField(max_length=150)
    bio = models.TextField(default="", null=True)
    age = models.IntegerField(default=None, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()
        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
