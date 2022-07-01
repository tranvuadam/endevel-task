import os

from django.db import models

# Create your models here.
from tag.models import Tag


def get_upload_path(instance, filename):
    return os.path.join(instance.title, filename)


def get_thumb_upload_path(instance, filename):
    return os.path.join(instance.title, "thumbnail", filename)


class BlogPost(models.Model):
    title = models.CharField("Title", max_length=150)
    detail = models.TextField("Detail", max_length=300)
    text = models.TextField("Text", max_length=3000)
    tags = models.ManyToManyField(Tag, related_name="blog_posts")
    image = models.ImageField("Image", upload_to=get_upload_path, default="default.jpg")
    thumbnail = models.ImageField("Thumbnail", upload_to=get_thumb_upload_path, default="default_thumb.jpg")

    def filename(self):
        return os.path.basename(self.image.name)