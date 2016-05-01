from django.db import models

from .managers import ThreegramManager


class Food(models.Model):
    name = models.TextField()

    objects = ThreegramManager

    def __unicode__(self):
        return self.name
