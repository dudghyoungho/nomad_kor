# models/anonymous.py

from django.db import models

class Anonymous(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 익명 게시판 이름

    def __str__(self):
        return self.name