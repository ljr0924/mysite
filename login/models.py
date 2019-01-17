from django.db import models

# Create your models here.

class Users(models.Model):
    user_name = models.CharField(max_length=10)
    user_password = models.CharField(max_length=255)
    user_ticket = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'day51_user'