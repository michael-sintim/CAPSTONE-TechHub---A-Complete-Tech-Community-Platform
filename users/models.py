from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Q,Count

# Create your models here.

class Skill(models.Model):
    name = models.CharField(max_length=150,unique=True)

    def __str__(self): return self.name

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProfileQuerySet(models.QuerySet): 
    def influencer(self):
        return self.filter(Q(is_active=True)&Q(reputation_score__gt = 500))
    
    def skill_hunting(self):
        return self.filter(Q(skills__name="Django"))
    
    def follower_count(self):
        return self.annotate(follower_count=Count('following')).filter(follower_count__gt = 10)
    
class PostQuerySet(models.QuerySet):
    def get_all_post(self):
        return self.select_related('user')
    
    def content_clean_up(self):
        return  self.filter(Q(body="")|Q(user__user_profile__is_active=False))
    

class Post(TimeStampModel):
    title = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    body =models.TextField(blank=True)

    def __str__(self):
        return self.title
    
    
    objects = PostQuerySet.as_manager()

class Profile(TimeStampModel):
    id = models.UUIDField(default=uuid.uuid4,editable=False, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'user_profile')
    skills = models.ManyToManyField(Skill, related_name="skills_profile")
    following = models.ManyToManyField('self',symmetrical=False,blank=True, related_name='following_profile')
    is_active = models.BooleanField(default=True)
    last_activity = models.DateTimeField(auto_now=True)
    urls = models.URLField(max_length=300,blank=True,null=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    reputation_score = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username
    
    objects = ProfileQuerySet.as_manager()

    class Meta:
        permissions = [
            ('can_verify_profile','Can verify user profile')
        ]
        db_table = 'profile'
        ordering = ['-created_at']
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        indexes = [
            models.Index(fields=['is_active','-created_at']),
            
        ]

class ActiveManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)
    
    def get_all_objects(self):
        return Profile.objects.filter(is_deleted = False)
    
    def create_user_with_profile(username,password):
