from django.db import models

class Bookmark(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField('urlurl', unique=True)

    def __str__(self):
        return self.title
