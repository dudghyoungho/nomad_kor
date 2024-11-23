# models/ftf.py

from django.db import models

class FTF(models.Model):
    name = models.CharField(max_length=100, unique=True)  # FTF 게시판 이름

    def __str__(self):
        return self.name
