import os

from PIL import Image
from django.core.files.images import ImageFile
from django.db import models

# Create your models here.
from tag.models import Tag


def get_upload_path(instance, filename):
    return os.path.join(instance.title, filename)


def get_thumb_upload_path(instance, filename):
    return os.path.join("thumbnails", filename)


class BlogPost(models.Model):
    title = models.CharField("Title", max_length=150)
    detail = models.TextField("Detail", max_length=300)
    text = models.TextField("Text", max_length=3000)
    tags = models.ManyToManyField(Tag, related_name="blog_posts")
    image = models.ImageField("Image", upload_to=get_upload_path, default="default.jpg")
    thumbnail = models.ImageField("Thumbnail", upload_to=get_thumb_upload_path, default="default_thumb.jpg")

    __original_image = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_image = self.image

    def __str__(self):
        return self.title

    def filename(self):
        return os.path.basename(self.image.name)

    def save(self, *args, **kwargs):
        # create copy
        if self.__original_image != self.image:
            self.thumbnail = ImageFile(self.image)
            super().save(*args, **kwargs)
            # resize thumbnail
            image = Image.open(self.thumbnail.path)
            output_size = [250, 250]
            image.thumbnail(output_size, Image.ANTIALIAS)
            if image.mode == "JPEG":
                image.save(self.thumbnail.path, format='JPEG')
            elif image.mode in ["RGBA", "P"]:
                image.save(self.thumbnail.path, format='PNG')
        else:
            super().save(*args, **kwargs)


