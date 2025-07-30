from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def str__(self):  # ✅ Fixed __str
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # ✅ added related_name
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # Optional but helpful
        return f'Comment by {self.author.username} on {self.post.title}'



class Image(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title=models.CharField(max_length=250)
    description=models.TextField(blank=True)
    image_file=models.ImageField(upload_to='uploads/images/')
    tags=models.CharField(max_length=200,blank=True, help_text="Comma-seperated-tags")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
