from email.policy import default
from operator import imod
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from ckeditor.fields import RichTextField

# Create your models here.

class Post(models.Model):
    sno = models.AutoField(primary_key=True) 
    title = models.CharField(max_length=260)
    catagory = models.CharField(max_length=20 , default="default")
    content = RichTextField(blank=True,null=True)
    author = models.CharField(max_length=13)
    timestamp = models.DateTimeField(blank=True , default=now)
    slug = models.CharField(max_length=120)
    image = models.ImageField(default="default")

    def __str__(self):
        return self.title + " by " + self.author

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE , null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username