from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.


class User(AbstractUser):
    warehouse_keeper = models.BooleanField('warehouse_keeper',default=False)
    technical = models.BooleanField('Technical Section',default=False)
    def get_edit_url(self):
        return reverse('edit_user',kwargs={'username':self.username})