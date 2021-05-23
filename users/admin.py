  
from django.contrib import admin
from .models import Profile
import users.models as users_models

admin.site.register(Profile)
admin.site.register(users_models.Document)
