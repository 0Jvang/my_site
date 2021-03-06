from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.timezone import now
import markdown


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField(default=now)  # auto_now_add=True(admin不显示、无法修改, 不更新）
    modified_time = models.DateTimeField(default=now)  # auto_now=True(admin不显示、无法修改, 自动更新)
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
#        if not self.excerpt:
 #           md = markdown.Markdown(extensions=[
  #              'markdown.extensions.extra',
   #             'markdown.extensions.codehilite',
    #        ])
     #       self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)
