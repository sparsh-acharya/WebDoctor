import uuid
from django.db import models
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from user.manager import UserManager
from EHR import settings



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)  # Add first name
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=100,unique=True,null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female') , ('Others', 'Others')])
    address = models.TextField(null=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
