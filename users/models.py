from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("DOCTOR", "Doctor"),
        ("NURSE", "Nurse"),
        ("RECEPTIONIST", "Receptionist"),
        ("LAB_TECH", "Lab Technician"),
        ("PHARMACIST", "Pharmacist"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True)