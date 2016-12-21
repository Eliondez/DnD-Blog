from django.db import models
from character.models import Character

class Achievment(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    img = models.FileField(upload_to='achievments_img/', null=True, blank=True)
    owners = models.ManyToManyField(Character)

    def __str__(self):
        return self.name

# Create your models here.
