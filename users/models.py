from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile')
    projects = models.ForeignKey(Project, on_delete="profile")
    skills = models.ManyToManyField(Skills, on_delete="profile")
    following = models.ManyToManyField(following, on_delete="profile")
    post = models.ForeignKey(Post,on_delete='profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user 