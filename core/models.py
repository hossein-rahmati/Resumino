from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Comment(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    content = models.TextField()
    job = models.CharField(max_length=255)
    counted_views = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    class Meta:
        ordering = ['created_date']
    def __str__(self):
        return self.title