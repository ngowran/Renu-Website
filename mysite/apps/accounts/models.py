from django.db import models

# Create your models here.

class UserProfile(models.Model):
  is_full_name_displayed = models.BooleanField(default=True)