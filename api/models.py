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


class FoodPhoto(models.Model):
    photo_url = models.CharField(max_length=300)
    feed_thumbnail_url = models.CharField(
        max_length=300, blank=True, null=True)
    map_thumbnail_url = models.CharField(
        max_length=300, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)

    def get_photo_url(self):
        if self.feed_thumbnail_url:
            return self.feed_thumbnail_url
        else:
            return self.photo_url
    
    def __str__(self):
        return self.photo_url


class Post(models.Model):
    user = models.ForeignKey(User)
    foodphoto = models.ForeignKey(FoodPhoto)
    last_update = models.DateTimeField('last updated', auto_now=True)
    create_time = models.DateTimeField('created', auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{0}_{1}'.format(self.create_time, self.description)


