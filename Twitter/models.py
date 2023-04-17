from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete= models.CASCADE)
    follows = models.ManyToManyField( "self" ,
                                     symmetrical=False,
                                     blank=True,
                                     related_name="followed_by")
    def __str__(self):
        return self.user.username
# Create your models here.
