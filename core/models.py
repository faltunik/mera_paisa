from django.db import models

# Create your models here.

class Item(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    access_token = models.CharField( max_length=500, null=True, blank=True)

    def __str__(self):
        return self.user.username
