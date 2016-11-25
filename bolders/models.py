from django.db import models
from django.core.urlresolvers import reverse

experience = {1:0,
              2:300,
              3:900,
              4:2700,
              5:6500,
              6:14000,
              7:23000,
              8:34000,
              9:48000,
              10:64000,
              11:85000,
              12:100000,
              13:120000,
              14:140000,
              15:165000}

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    ingamedate = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'id': self.id})


class Character(models.Model):
    name = models.CharField(max_length=200)
    char_class = models.CharField(max_length=100)
    level = models.IntegerField()
    exp = models.IntegerField()
    description = models.TextField()
    photo = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name

    def to_next_level(self):
        curr_level_exp = experience[self.level]
        next_level_exp = experience[self.level + 1]
        need_exp = next_level_exp - curr_level_exp
        extra_exp = self.exp - curr_level_exp
        return (extra_exp * 100)//need_exp