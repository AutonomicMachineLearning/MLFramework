from django.db import models

# Create your models here.
class Table (models.Model) :
    name = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    office = models.CharField(max_length=100, blank=True, null=True)
    age = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateTimeField('start date', auto_now_add=True)
    salary = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
