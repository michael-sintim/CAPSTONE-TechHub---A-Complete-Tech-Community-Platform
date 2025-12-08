from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Skill(models.Model):
    name = models.CharField(max_length=150,unique=True)
    def __str__(self): return self.name

class Post(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'user_profile')
    skills = models.ManyToManyField(Skill, related_name="skills_profile")
    following = models.ManyToManyField('self',symmetrical=False,blank=True, related_name='following_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    last_activity = models.DateTimeField(auto_now=True)
    urls = models.URLField(max_length=300)
    id = models.UUIDField(default=uuid.uuid4,editable=False, primary_key=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    reputation_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username
    

    class Meta:
        permissions = [
            ('can_verify_profile','Can verify user profile')
        ]