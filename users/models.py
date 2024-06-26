from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from results import *

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #CASCADE -> Delete profile is user is deleted but not vice versa
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    # def get_results(self):
    #     """
    #     Method to get all results associated with this user.
    #     """
    #     return Result.objects.filter(user=self)


    
    # Note -> to view profile in our database, we must register it in admin.py
    
    #allows us to diplsa profile object acc our needs
    def __str__(self):
        return f'{self.user.username} Profile'
    
    # scales down the image for better performance
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # import image using pillow library
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)