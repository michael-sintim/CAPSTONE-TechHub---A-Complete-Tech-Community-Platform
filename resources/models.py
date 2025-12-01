from django.db import models
from users.models import User
from projects.models import Category
# Create your models here.
class Resource(models.Model):
    class Difficulty(models.TextChoices):
        BEGINNER ='BEGINNER','Beginner'
        INTERMEDIATE ='INTERMEDIATE','Intermediate'
        ADVANCED ='ADVANCED','Advanced'
    title =models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='authored_resources')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="category_resource")
    difficulty = models.CharField(choices=Difficulty.choices, default=Difficulty.BEGINNER,max_length=20)
    bookmarked_by = models.ManyToManyField(User,related_name= "bookmarkby_resource", blank=True)
    urls= models.URLField()

class Rating(models.Model):
    rating = models.IntegerField()
    def __str__(self):
        return f'{self.author.username} - {self.title}'