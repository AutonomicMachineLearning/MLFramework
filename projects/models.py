from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Projects (models.Model) :
    # name = models.CharField(max_length=100, blank=True, null=True)
    projectName = models.CharField(max_length=100, blank=True, null=True)
    projectDescription = models.TextField('DESCRIPTION', blank=True, null=True)
    projectTag = models.TextField('PROJECT TAG', blank=True, null=True)
    cretae_date = models.DateTimeField('Create Date', auto_now=True)
    modify_date = models.DateTimeField('Modify Date', auto_now=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.projectName