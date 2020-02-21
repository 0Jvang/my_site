from django.db import models
from django.utils.timezone import now


# Create your models here.
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(default=now)
    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]
