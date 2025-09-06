from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser # By us
from django.db import models # Alredy Present

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('passenger', 'Passenger'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='passenger')

    def __str__(self):
        return f"{self.username} ({self.role})"
