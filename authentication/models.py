from distutils.command.upload import upload
from email.policy import default
from enum import unique
from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser


# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = "username"
    REQUIRED_FIELD = ["first_name", "last_name"]
    is_email_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    profileimage = models.ImageField(
        upload_to="profileimg", default="user.png", null=True, blank=True
    )

    objects = UserManager()
    def str(self):
        return self.email
    