from django.db import models

class Board(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 게시판 이름

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"

