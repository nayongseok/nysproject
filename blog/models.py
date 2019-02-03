from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('blog.Post', related_name='comments',on_delete=models.CASCADE) 

    def __str__(self):
        return self.text

