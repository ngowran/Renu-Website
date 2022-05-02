from django.contrib import admin

from .models import UserProfile, UserPersona

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(UserPersona)