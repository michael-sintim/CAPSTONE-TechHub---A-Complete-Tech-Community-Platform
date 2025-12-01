from django.db import models
from projects.models import Project, User
from bugs.models import Bug
# Create your models here.
class Bug(models.Model):
    class Priority(models.TextChoices):
        HIGH = 'HIGH','HIGH'
        MEDIUM = 'MEDIUM','MEDIUM'
        LOW = 'LOW','LOW'
        CRITICAL = 'CRITICAL','critical'

    class Status(models.TextChoices):
        OPEN = 'OPEN','OPEN'
        IN_PROGRESS = 'IN_PROGRESS','IN PROGRESS'
        RESOLVED = 'RESOLVED','RESOLVED'
        CLOSED ='CLOSED','CLOSED'
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=300)
    resolved_at = models.DateTimeField(null=True)
    file_attachment = models.ImageField(null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='project_bugs')
    reporter =  models.ForeignKey(User,on_delete=models.CASCADE,related_name='reporter_bugs')
    assigned_to = models.ForeignKey(User,null=True,blank=True,related_name="assignedTo_bug")
    status = models.CharField(choices=Status.choices, default=Status.OPEN, max_length=12)
    priority = models.CharField(choices=Priority.choices,default=Priority.LOW,max_length=10)
    bug_history = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name='history_bug')

    def __str__(self):
        return self.reporter.username