from django.db import models

# Create your models here.
from tag.models import Tag


class BlogPost(models.Model):
    title = models.CharField("Title", max_length=150)
    detail = models.TextField("Detail", max_length=300)
    text = models.TextField("Text", max_length=3000)
    tags = models.ManyToManyField(Tag, related_name="blog_posts")