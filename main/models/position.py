
from django.db import models

class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Position name

    def __str__(self):
        return self.name

