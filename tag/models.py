from django.db import models


# Create your models here.
class Tag(models.Model):
    name = models.CharField("Tag name", max_length=100)

    def __str__(self):
        return self.name
