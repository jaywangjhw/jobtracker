from django.contrib import admin
from .models import Company, Position, Account


admin.site.register(Position)
admin.site.register(Company)
admin.site.register(Account)
