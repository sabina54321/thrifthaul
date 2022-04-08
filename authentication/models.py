from email.policy import default
from django.db import models
from django.contrib.auth.models import (UserManager,AbstractUser)


# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD='username'
    REQUIRED_FIELD=['first_name','last_name']
    is_email_verified = models.BooleanField(default=False)

    objects = UserManager()
    def str(self):
        return self.email