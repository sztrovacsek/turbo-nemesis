from django.db import models
from django.contrib.auth.models import User


class FacebookUser(models.Model):
    fb_name = models.CharField(max_length=100)
    fb_first_name = models.CharField(max_length=100)
    fb_last_name = models.CharField(max_length=100)
    fb_email = models.CharField(max_length=200)
    user_id = models.ForeignKey(User)
    
    def __str__(self):
        return self.fb_name

