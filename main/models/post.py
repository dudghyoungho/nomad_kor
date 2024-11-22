from django.db import models
from . import Board
from .profile import Profile  # Profile 모델을 import

class Post(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Profile 객체를 author로 설정
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
