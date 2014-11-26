from django.contrib import admin

from .models import *


admin.site.register(FacebookUser)
admin.site.register(FoodPhoto)
admin.site.register(Post)

