from django.contrib import admin
from .models import Company, Position


admin.site.register(Position)
admin.site.register(Company)