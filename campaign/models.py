from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from accounts.models import Profile

class Campaign(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название кампании')
    master = models.ForeignKey(Profile, null=True,blank=True)
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

class Story(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    ingamedate = models.DateField(blank=False)
    posted = models.DateTimeField(auto_now_add=False, null=True)
    campaign = models.ForeignKey(Campaign, null=True)

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
