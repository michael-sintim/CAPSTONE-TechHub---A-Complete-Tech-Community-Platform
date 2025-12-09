from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


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
    file_attachment = models.FileField(validators=
                                       [FileExtensionValidator('pdf','jpeg','zip')],blank=True,null=True,upload_to='bug_reports/')
    project = models.ForeignKey("projects.Project",on_delete=models.CASCADE,related_name='project_bugs')
    reporter =  models.ForeignKey(User,on_delete=models.CASCADE,related_name='reporter_bugs')
    assigned_to = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,related_name="assignedTo_bug")
    status = models.CharField(choices=Status.choices, default=Status.OPEN, max_length=12)
    priority = models.CharField(choices=Priority.choices,default=Priority.LOW,max_length=10)

    def __str__(self):
        return self.reporter.username
    
class BugHistory(models.Model):
    bug = models.ForeignKey('bugs.Bug', on_delete=models.CASCADE, related_name='history')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)