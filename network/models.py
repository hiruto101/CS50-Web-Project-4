from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    content = models.CharField(max_length= 300)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="likes")
    
    def like_count(self):
        return len(self.likes.count())
    
    def __str__(self):
        likes_count = self.likes.count()
        return f"ID: {self.pk} User: {self.author} Post: {self.content} Date: {self.date.strftime('%d %b %Y %H:%M:%S')} Likes: {likes_count}"
    
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    
    class Meta:
        unique_together = ('user', 'post')