from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from resources.models import Resource

class Category(models.Model):
    name = models.CharField(max_length=130)

class Project(models.Model):
    class Status(models.TextChoices):
        PLANNING = 'PLANNING','planning'
        ACTIVE = 'ACTIVE','active'
        ON_HOLD = 'ON_HOLD','on hold'
        COMPLETED = 'COMPLETED','completed'
        ARCHIVED = 'ARCHIVED','archived'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project')
    contributors = models.ManyToManyField(User,related_name='contributed_project')
    technologies = models.CharField(max_length=150)
    upvotes = models.ManyToManyField(User,related_name='upvotes_project')
    title = models.CharField(max_length=150)    
    description = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    resource = models.ManyToManyField(Resource, blank=True, related_name="resource_project")
    is_public = models.BooleanField(default=True)
    start_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=21,choices=Status.choices, default=Status.PLANNING)

    def __str__(self):
        return self.title
    


class Tag(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
