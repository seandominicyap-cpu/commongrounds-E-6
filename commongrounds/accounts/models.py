from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(User):
    display_name = models.CharField(max_length=63)
    email_address = models.EmailField()