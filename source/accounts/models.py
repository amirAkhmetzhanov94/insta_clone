from django.db import models
from django.contrib.auth import get_user_model


class Gender(models.Model):
    gender = models.CharField(max_length=15, verbose_name="Gender")

    def __str__(self):
        return f'{self.gender}'


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name="profile", on_delete=models.CASCADE, verbose_name="User")

    avatar = models.ImageField(blank=False, upload_to="avatars", verbose_name="Avatar")

    about = models.TextField(max_length=150, blank=True, null=True, verbose_name="About user")

    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone number")

    gender_user = models.ForeignKey(Gender, blank=True, null=True, on_delete=models.PROTECT, verbose_name="Gender user")

    followers = models.ManyToManyField(get_user_model(), blank=True, related_name="subscriptions")

    following = models.ManyToManyField(get_user_model(), blank=True, related_name="followings")

    def __str__(self):
        return f'{self.user}'






