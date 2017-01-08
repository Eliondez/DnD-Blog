from django.db import models
from django.core.urlresolvers import reverse
from accounts.models import Profile
from taggit.managers import TaggableManager
from precise_bbcode.fields import BBCodeTextField

class Campaign(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название кампании')
    master = models.ForeignKey(Profile, null=True,blank=True)

    rp_system = models.CharField(max_length=50,
                             default='Нет',
                             verbose_name='Система')

    description = models.TextField(verbose_name='Описание кампании')
    started = models.DateField(null=True, blank=True, verbose_name='Дата начала')
    ended = models.DateField(null=True, blank=True, verbose_name='Дата окончания')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('campaign:campaign_detail', kwargs={'id': self.id})

class Story(models.Model):
    class Meta:
        ordering = ['-ingamedate', '-posted']

    title = models.CharField(max_length=200, verbose_name='Название')
    content = models.TextField(verbose_name='Содержание')
    ingamedate = models.DateField(blank=False, verbose_name='Внутриигровая дата')
    posted = models.DateTimeField(auto_now_add=True, null=True, help_text='Формат ГГГГ-ММ-ДД')
    campaign = models.ForeignKey(Campaign, null=True)
    tags = TaggableManager(blank=True, verbose_name='Теги')

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
        return reverse('campaign:detail_story', kwargs={'campaign_id': self.campaign.id, 'story_id': self.id})
