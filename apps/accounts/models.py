from django.contrib.auth.models import AbstractUser
from django.db import models


class PassSafeUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    master_password_hint = models.CharField(
        max_length=255,
        blank=True,
        help_text='Hint for the master password',
    )

    def __str__(self):
        return self.username
