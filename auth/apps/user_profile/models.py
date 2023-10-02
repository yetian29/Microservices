from django.db import models
from django.conf  import settings
from djoser.signals import user_registered

User = settings.AUTH_USER_MODEL

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(default='media/users/user_default_profile.png', upload_to='media/users/pictures/', blank=True, null=True, verbose_name='Picture')
    banner = models.ImageField(default='media/users/user_default_bg.png', upload_to='media/users/banners/', blank=True, null=True, verbose_name='Banner')
    location = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    profile_info = models.TextField(max_length=200, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    github = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.CharField(max_length=100, blank=True, null=True)


def post_user_registered(request, user, *args, **kwargs):

    user = user
    UserProfile.objects.create(user=user)

user_registered.connect(post_user_registered)












 