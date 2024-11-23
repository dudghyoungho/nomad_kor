from django.db import models
from .post import Post  # 게시글 모델
from .profile import Profile  # 프로필 모델

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # 댓글이 속한 게시글
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)  # 댓글 작성자
    author_name = models.CharField(max_length=100)  # 댓글 작성자 이름
    content = models.TextField()  # 댓글 내용
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)  # 대댓글
    is_private = models.BooleanField(default=False)  # 비밀 댓글 여부
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일

    def __str__(self):
        return f"Comment by {self.author_name} on {self.post.title}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

