from django.conf import settings
from django.db import models


class Category(models.TextChoices):
    SOCIAL = 'social', 'Social'
    FINANCE = 'finance', 'Banca'
    WORK = 'work', 'Trabajo'
    SHOPPING = 'shopping', 'Compras'
    OTHER = 'other', 'Otros'


class Credential(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credentials')
    service_name = models.CharField(max_length=120)
    category = models.CharField(max_length=32, choices=Category.choices, default=Category.OTHER)
    url = models.URLField(blank=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.service_name} ({self.username})'
