from django.db import models

class Post(models.Model):
    slug  = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.title
