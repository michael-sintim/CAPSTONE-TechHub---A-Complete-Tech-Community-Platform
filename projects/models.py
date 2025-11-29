from django.db import models
from users.models import User
# Create your models here.
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project')
    contributors = models.ManyToManyField(User, on_delete=models.CASCADE)
    technologies = models.CharField(max_length=150)
    bugs = models.ForeignKey(Bugs, on_delete=models.CASCADE,related_name='bugs')
    upvotes = models.ManyToManyField(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=120)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Tags(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
