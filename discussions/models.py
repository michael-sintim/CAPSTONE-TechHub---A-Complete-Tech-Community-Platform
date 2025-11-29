from django.db import models
from projects.models import Category, User,Project
# Create your models here.
class Discussion(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='discussion')
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='discussion')
    replies = models.ManyToManyField(User,)
    following = models.ManyToManyField(User,related_name='discussions',)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)

    def __str__(self):
        return self.category
    