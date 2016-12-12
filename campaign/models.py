from django.db import models
from django.core.urlresolvers import reverse

class Campaign(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название кампании')
    PR_SYSTEM_CHOICES = (
        ('no', 'None'),
        ('gp', 'GURPS'),
        ('d5e', 'DnD 5e'),
    )

    rp_system = models.CharField(max_length=5,
                             choices = PR_SYSTEM_CHOICES,
                             default='no',
                             verbose_name='Система')

    description = models.TextField(verbose_name='Описание кампании')
    started = models.DateField(null=True, blank=True, verbose_name='Дата начала')
    ended = models.DateField(null=True, blank=True, verbose_name='Дата окончания')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('campaign_detail', kwargs={'id': self.id})



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

class Story(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    ingamedate = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def get_next(self):
        next = Story.objects.filter(id__gt=self.id)
        if next:
            return next.first()
        return False

    def get_prev(self):
        prev = Story.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first()
        return False

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'id': self.id})


class Character(models.Model):
    name = models.CharField(max_length=200)
    char_class = models.CharField(max_length=100)
    exp = models.IntegerField()
    description = models.TextField()
    photo = models.FileField(null=True, blank=True)
    photo_full = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_current_level(self):
        level = 0
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

class Achievment(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    img = models.FileField(upload_to='achievments_img/', null=True, blank=True)
    owners = models.ManyToManyField('Character')

    def __str__(self):
        return self.name


