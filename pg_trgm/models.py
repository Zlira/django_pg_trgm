from django.db import models


class Food(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name
