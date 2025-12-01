from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Discussion(models.Model):
    category = models.ForeignKey('projects.Category', on_delete=models.CASCADE, related_name='discussion')
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='discussion')
    replies = models.ForeignKey('self',blank=True,on_delete=models.CASCADE)
    following = models.ManyToManyField(User,related_name='discussions',)
    tag = models.ManyToManyField('projects.Tag',blank=True)
    voting = models.ManyToManyField(User,related_name='voting_Discussion')


    def __str__(self):
        return self.category
    