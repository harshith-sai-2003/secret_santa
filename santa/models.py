from django.db import models

# Create your models here.

class Room(models.Model):
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)


class Participant(models.Model):
    name = models.CharField(max_length=100, default="")  # Default empty string
    isPresentInBangalore = models.BooleanField(default=False)  # Default False
    address = models.TextField(default="")  # Default empty string
    email = models.EmailField(default="")  # Default empty string
    phone = models.CharField(max_length=15, default="")  # Default empty string
    budget = models.IntegerField(default=0)  # Default to 0
    hobby = models.CharField(max_length=100, default="")  # Default empty string

    def __str__(self):
        return self.name