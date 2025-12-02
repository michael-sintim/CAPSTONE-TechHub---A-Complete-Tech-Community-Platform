from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=130)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)

    def __str__(self):
        return self.name
    
class Project(models.Model):
    class Status(models.TextChoices):
        PLANNING = 'PLANNING','planning'
        ACTIVE = 'ACTIVE','active'
        ON_HOLD = 'ON_HOLD','on hold'
        COMPLETED = 'COMPLETED','completed'
        ARCHIVED = 'ARCHIVED','archived'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    contributors = models.ManyToManyField(User,related_name='contributed_projects',blank=True)
    technologies = models.ManyToManyField(Tag,blank=True)
    upvotes = models.ManyToManyField(User,related_name='upvotes_projects',blank=True)
    title = models.CharField(max_length=150)    
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='cateogory_projects')
    resource = models.ManyToManyField('resources.Resource', blank=True, related_name="resource_projects")
    is_public = models.BooleanField(default=True)
    start_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=21,choices=Status.choices, default=Status.PLANNING)

    def __str__(self):
        return self.title
    
class ProjectImage(models.Model):
    project= models.ForeignKey(Project, on_delete=models.CASCADE, related_name="projectImage")
    image = models.ImageField(upload_to='project_gallery/')

    def __str__(self):
        return f"Image for {self.project.technologies}"
    
    

