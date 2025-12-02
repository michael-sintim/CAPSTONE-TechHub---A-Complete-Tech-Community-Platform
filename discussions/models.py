from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Discussion(models.Model):
    category = models.ForeignKey('projects.Category', on_delete=models.CASCADE, related_name='discussion')
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='author_discussion')
    parent = models.ForeignKey('self',blank=True,null=True,on_delete=models.CASCADE,related_name='replies')
    following = models.ManyToManyField(User,related_name='following_discussion',)
    tags = models.ManyToManyField('projects.Tag',blank=True)
    voting = models.ManyToManyField(User,related_name='voting_discussion')
    title = models.CharField(max_length=150)
    content = models.TextField()



    def __str__(self):
        return self.title
    