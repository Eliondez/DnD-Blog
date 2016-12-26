from django.db import models
from django.core.urlresolvers import reverse

from campaign.models import Campaign
from accounts.models import Profile

experience_levels = {1:0,
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

class Character(models.Model):
    name = models.CharField(max_length=200)
    char_class = models.CharField(max_length=100)
    exp = models.IntegerField()
    description = models.TextField()
    photo = models.FileField(null=True, blank=True)
    photo_full = models.FileField(null=True, blank=True)
    campaign = models.ForeignKey(Campaign, null=True, blank=True)
    owner = models.ForeignKey(Profile, null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            this_record = Character.objects.get(id = self.id)
            if this_record.photo != self.photo:
                this_record.photo.delete(save = False)
            if this_record.photo_full != self.photo_full:
                this_record.photo_full.delete(save = False)
        except:
            pass
        super(Character, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.photo.delete(save = False)
        self.photo_full.delete(save = False)
        super(Character, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_current_level(self):
        level = 1
        for key, val in experience_levels.items():
            if self.exp > val:
                level = int(key)
            else:
                break
        return level

    def to_next_level(self):
        current_level = self.get_current_level()
        curr_level_exp = experience_levels[current_level]
        next_level_exp = experience_levels[current_level + 1]
        need_exp = next_level_exp - curr_level_exp
        extra_exp = self.exp - curr_level_exp
        return (extra_exp * 100)//need_exp

    def get_absolute_url(self):
        return reverse('char_detail', kwargs={'id': self.id})