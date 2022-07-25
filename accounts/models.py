from django.contrib.auth.models import AbstractUser, UserManager


# Create your models here.

class Shopper(AbstractUser):

    objects = UserManager()


  
