from django.db import models

# Create your models here.

class NeSIUser(models.Model):
    username = models.CharField(max_length=20)
    token = models.CharField(max_length=30)
    provider = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    def qualifiedName(self):
        return self.username  + "@" + self.provider
    
class Request(models.Model):
    user = models.ForeignKey(NeSIUser)
    message = models.TextField()

class Project(models.Model):
    vo = models.CharField(max_length=200)
    label = models.CharField(max_length=200)
    description = models.TextField()
    