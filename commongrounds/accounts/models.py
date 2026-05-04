from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role)
    display_name = models.CharField(max_length=63)
    email_address = models.EmailField()

    def __str__(self):
<<<<<<< HEAD
        return self.display_name
=======
        if self.display_name:
            return self.display_name
        return self.user.username
>>>>>>> merchstore_final
